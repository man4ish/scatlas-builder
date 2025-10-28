from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.tables import Dataset
from app.services import preprocessing, clustering

router = APIRouter(prefix="/integrate", tags=["integrate"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/run/{dataset_id}")
def run_pipeline(dataset_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    ds = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if ds is None:
        raise HTTPException(status_code=404, detail="Dataset not found")

    # schedule background task
    background_tasks.add_task(_process_dataset, ds.id)
    return {"message": "Processing started", "dataset_id": ds.id}

def _process_dataset(dataset_id: int):
    db = SessionLocal()
    try:
        ds = db.query(Dataset).filter(Dataset.id == dataset_id).first()
        if not ds:
            return
        file_path = f"data/uploads/{ds.filename}"
        # preprocessing: read, QC, normalize
        adata = preprocessing.load_input(file_path)
        adata = preprocessing.run_qc_and_normalize(adata)
        adata = preprocessing.run_pca_umap(adata)
        # clustering
        adata = clustering.run_leiden(adata)
        # save processed AnnData to disk (h5ad)
        processed_path = f"data/uploads/processed_{ds.filename}.h5ad"
        adata.write(processed_path)
        # mark processed
        ds.processed = 1
        db.add(ds)
        db.commit()
    except Exception as e:
        # ideally log
        print("Error processing dataset:", e)
    finally:
        db.close()
