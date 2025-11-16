"""
app.routers.integrate
--------------------

This module defines the FastAPI router for integrating single-cell RNA-seq datasets
into the Single-Cell Atlas Builder pipeline. It provides endpoints to trigger
dataset preprocessing, dimensionality reduction (PCA, UMAP), clustering (Leiden),
and saving of processed AnnData objects.

The integration is performed in the background using FastAPI's BackgroundTasks,
allowing large datasets to be processed asynchronously. Processed datasets are
marked in the database for downstream visualization and analysis.

Key Functions:
- get_db(): Provides a SQLAlchemy session for dependency injection.
- run_pipeline(dataset_id, background_tasks, db): Starts background processing of a dataset.
- _process_dataset(dataset_id): Internal function performing preprocessing, dimensionality
  reduction, clustering, and saving processed datasets.

Dependencies:
- FastAPI
- SQLAlchemy
- Scanpy / AnnData (via app.services.preprocessing and clustering)
"""

from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.tables import Dataset
from app.services import preprocessing, clustering

router = APIRouter(prefix="/integrate", tags=["integrate"])


def get_db() -> Session:
    """
    Provides a SQLAlchemy database session for FastAPI dependency injection.
    Closes the session automatically after use.

    Returns:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/run/{dataset_id}")
def run_pipeline(dataset_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Starts the integration pipeline for a dataset in the background.

    Args:
        dataset_id (int): ID of the dataset to process
        background_tasks (BackgroundTasks): FastAPI background tasks manager
        db (Session): SQLAlchemy session dependency

    Returns:
        dict: Confirmation message with dataset_id
    """
    ds = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if ds is None:
        raise HTTPException(status_code=404, detail="Dataset not found")

    # Schedule the dataset processing as a background task
    background_tasks.add_task(_process_dataset, ds.id)
    return {"message": "Processing started", "dataset_id": ds.id}


def _process_dataset(dataset_id: int) -> None:
    """
    Internal function to process a dataset:
    1. Load raw data from CSV or H5AD
    2. Perform QC filtering, normalization, PCA, and UMAP
    3. Apply Leiden clustering and rank genes per cluster
    4. Save processed AnnData to disk
    5. Update database to mark dataset as processed

    Args:
        dataset_id (int): ID of the dataset to process
    """
    db = SessionLocal()
    try:
        ds = db.query(Dataset).filter(Dataset.id == dataset_id).first()
        if not ds:
            print(f"Dataset {dataset_id} not found in DB.")
            return

        file_path = f"data/uploads/{ds.filename}"

        # Preprocessing
        adata = preprocessing.load_input(file_path)
        adata = preprocessing.run_qc_and_normalize(adata)
        adata = preprocessing.run_pca_umap(adata)

        # Clustering
        adata = clustering.run_leiden(adata)

        # Save processed data
        processed_path = f"data/uploads/processed_{ds.filename}.h5ad"
        adata.write(processed_path)

        # Mark dataset as processed
        ds.processed = 1
        db.add(ds)
        db.commit()

    except Exception as e:
        print(f"Error processing dataset {dataset_id}: {e}")
    finally:
        db.close()
