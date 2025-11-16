"""
app.routers.visualize
--------------------

This module defines the FastAPI router for visualizing processed single-cell RNA-seq datasets.
It currently provides an endpoint to generate a UMAP plot from a preprocessed AnnData object
and returns the plot as a base64-encoded PNG image.

Dependencies:
- FastAPI
- SQLAlchemy
- Scanpy
- Matplotlib
- Base64 encoding for returning images via API
"""

import os
import base64
from io import BytesIO

import scanpy as sc
import matplotlib.pyplot as plt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.tables import Dataset

router = APIRouter(prefix="/visualize", tags=["visualize"])


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


@router.get("/umap/{dataset_id}")
def get_umap_plot(dataset_id: int, db: Session = Depends(get_db)):
    """
    Generate a UMAP plot for a preprocessed single-cell dataset.

    Loads the processed AnnData object for the given dataset ID, generates a UMAP
    plot using Scanpy, and returns the image as a base64-encoded PNG string.

    Args:
        dataset_id (int): The ID of the dataset to visualize
        db (Session): SQLAlchemy database session (dependency)

    Raises:
        HTTPException 404: If the dataset is not found or not yet processed
        HTTPException 404: If the processed file does not exist on disk

    Returns:
        dict: A dictionary containing the base64-encoded PNG image under the key "image_base64"
    """
    # Retrieve dataset entry from DB
    ds = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not ds or ds.processed == 0:
        raise HTTPException(status_code=404, detail="Processed dataset not found")

    # Build path to processed h5ad file
    processed_path = f"data/uploads/processed_{ds.filename}.h5ad"
    if not os.path.exists(processed_path):
        raise HTTPException(status_code=404, detail="Processed file not found")

    # Load processed AnnData object
    adata = sc.read_h5ad(processed_path)

    # Generate UMAP plot without showing it
    fig = sc.pl.umap(adata, show=False)

    # Save figure to in-memory buffer
    buf = BytesIO()
    fig.figure.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig.figure)
    buf.seek(0)

    # Encode image as base64
    img_b64 = base64.b64encode(buf.read()).decode("utf-8")

    return {"image_base64": img_b64}

@router.get("/gene_expression/{dataset_id}")
def get_gene_expression_plot(
    dataset_id: int,
    gene: str,
    db: Session = Depends(get_db)
):
    """
    Generate a UMAP plot colored by expression of a specified gene.

    Loads the processed AnnData object for the given dataset ID, colors the UMAP
    plot by the expression of the requested gene, and returns the image as a base64-encoded PNG.

    Args:
        dataset_id (int): The ID of the dataset to visualize
        gene (str): The gene name to color by
        db (Session): SQLAlchemy database session (dependency)

    Raises:
        HTTPException 404: If the dataset is not found or not yet processed
        HTTPException 404: If the processed file does not exist on disk
        HTTPException 400: If the specified gene is not present in the dataset

    Returns:
        dict: A dictionary containing the base64-encoded PNG image under the key "image_base64"
    """
    # Retrieve dataset entry from DB
    ds = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not ds or ds.processed == 0:
        raise HTTPException(status_code=404, detail="Processed dataset not found")

    # Build path to processed h5ad file
    processed_path = f"data/uploads/processed_{ds.filename}.h5ad"
    if not os.path.exists(processed_path):
        raise HTTPException(status_code=404, detail="Processed file not found")

    # Load processed AnnData object
    adata = sc.read_h5ad(processed_path)

    # Check if gene exists
    if gene not in adata.var_names:
        raise HTTPException(status_code=400, detail=f"Gene '{gene}' not found in dataset")

    # Generate UMAP plot colored by gene expression
    fig = sc.pl.umap(adata, color=gene, show=False)

    # Save figure to in-memory buffer
    buf = BytesIO()
    fig.figure.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig.figure)
    buf.seek(0)

    # Encode image as base64
    img_b64 = base64.b64encode(buf.read()).decode("utf-8")

    return {"image_base64": img_b64}

@router.get("/gene_expression/{dataset_id}")
def get_gene_expression_plot(
    dataset_id: int,
    gene: str,
    db: Session = Depends(get_db)
):
    """
    Generate a UMAP plot colored by expression of a specified gene.

    Loads the processed AnnData object for the given dataset ID, colors the UMAP
    plot by the expression of the requested gene, and returns the image as a base64-encoded PNG.

    Args:
        dataset_id (int): The ID of the dataset to visualize
        gene (str): The gene name to color by
        db (Session): SQLAlchemy database session (dependency)

    Raises:
        HTTPException 404: If the dataset is not found or not yet processed
        HTTPException 404: If the processed file does not exist on disk
        HTTPException 400: If the specified gene is not present in the dataset

    Returns:
        dict: A dictionary containing the base64-encoded PNG image under the key "image_base64"
    """
    # Retrieve dataset entry from DB
    ds = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not ds or ds.processed == 0:
        raise HTTPException(status_code=404, detail="Processed dataset not found")

    # Build path to processed h5ad file
    processed_path = f"data/uploads/processed_{ds.filename}.h5ad"
    if not os.path.exists(processed_path):
        raise HTTPException(status_code=404, detail="Processed file not found")

    # Load processed AnnData object
    adata = sc.read_h5ad(processed_path)

    # Check if gene exists
    if gene not in adata.var_names:
        raise HTTPException(status_code=400, detail=f"Gene '{gene}' not found in dataset")

    # Generate UMAP plot colored by gene expression
    fig = sc.pl.umap(adata, color=gene, show=False)

    # Save figure to in-memory buffer
    buf = BytesIO()
    fig.figure.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig.figure)
    buf.seek(0)

    # Encode image as base64
    img_b64 = base64.b64encode(buf.read()).decode("utf-8")

    return {"image_base64": img_b64}


