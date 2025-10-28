import os
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
from app.database import SessionLocal
from app.tables import Dataset
from app.schemas import DatasetCreate, DatasetOut

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
async def upload_dataset(file: UploadFile = File(...), name: str = None, metadata: str = None, db: Session = Depends(get_db)):
    if not name:
        raise HTTPException(status_code=400, detail="Name is required")
    ext = file.filename.split(".")[-1].lower()
    if ext not in {"h5ad", "csv", "loom", "mtx"}:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    uid = f"{uuid4().hex}.{ext}"
    path = os.path.join(UPLOAD_DIR, uid)
    with open(path, "wb") as f:
        content = await file.read()
        f.write(content)

    ds = Dataset(
        name=name,
        filename=uid,
        file_type=ext,
        metadata=metadata or ""
    )
    db.add(ds)
    db.commit()
    db.refresh(ds)
    return ds
