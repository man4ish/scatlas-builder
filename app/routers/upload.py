import os
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
from app.database import SessionLocal
from app.tables import Dataset
from app.schemas import DatasetCreate, DatasetOut
from app.utils.file_utils import save_uploaded_file   # <-- Add this line


router = APIRouter(prefix="/upload", tags=["upload"])

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
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
    if not name:
        raise HTTPException(status_code=400, detail="Name is required")

    allowed_exts = {"h5ad", "csv", "loom", "mtx"}
    ext = file.filename.split(".")[-1].lower()
    if ext not in allowed_exts:
        raise HTTPException(status_code=400, detail=f"Unsupported file type. Allowed: {allowed_exts}")

    # Save the file and get the unique filename
    try:
        unique_name, file_path = await save_uploaded_file(file)  # <- returns unique_name
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    # Create dataset entry
    ds = Dataset(
        name=name,
        filename=unique_name,  # <- now defined
        file_type=ext,
        meta_info=metadata or ""
    )
    db.add(ds)
    db.commit()
    db.refresh(ds)

    return ds