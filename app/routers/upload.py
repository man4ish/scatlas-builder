"""
app.routers.upload
------------------

This module defines the FastAPI router for uploading single-cell RNA-seq datasets
to the Single-Cell Atlas Builder. It provides endpoints to upload files in 
formats like H5AD, CSV, Loom, and MTX, stores them with unique names, and
creates corresponding entries in the database.

Dependencies:
- FastAPI
- SQLAlchemy
- UUID for generating unique file identifiers
- app.utils.file_utils.save_uploaded_file for secure file saving
- app.tables.Dataset and app.schemas.DatasetOut
"""

import os
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
from app.database import SessionLocal
from app.tables import Dataset
from app.schemas import DatasetCreate, DatasetOut
from app.utils.file_utils import save_uploaded_file

router = APIRouter(prefix="/upload", tags=["upload"])

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


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


@router.post("/", response_model=DatasetOut)
async def upload_dataset(
    file: UploadFile = File(...),
    name: str = None,
    metadata: str = None,
    db: Session = Depends(get_db)
):
    """
    Endpoint to upload a single-cell RNA-seq dataset.

    The uploaded file is validated for allowed extensions (h5ad, csv, loom, mtx),
    saved to the server with a unique name, and a corresponding Dataset entry is 
    created in the database.

    Args:
        file (UploadFile): File uploaded by the user
        name (str): Human-readable dataset name (required)
        metadata (str, optional): Additional metadata for the dataset
        db (Session): SQLAlchemy session dependency

    Raises:
        HTTPException 400: If name is missing or file type is unsupported
        HTTPException 500: If saving the file fails

    Returns:
        DatasetOut: The database record of the uploaded dataset
    """
    if not name:
        raise HTTPException(status_code=400, detail="Name is required")

    allowed_exts = {"h5ad", "csv", "loom", "mtx"}
    ext = file.filename.split(".")[-1].lower()
    if ext not in allowed_exts:
        raise HTTPException(status_code=400, detail=f"Unsupported file type. Allowed: {allowed_exts}")

    # Save the file and get the unique filename
    try:
        unique_name, file_path = await save_uploaded_file(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    # Create dataset entry in DB
    ds = Dataset(
        name=name,
        filename=unique_name,
        file_type=ext,
        meta_info=metadata or ""
    )
    db.add(ds)
    db.commit()
    db.refresh(ds)

    return ds
