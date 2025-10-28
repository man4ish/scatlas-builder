from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.tables import Dataset
import os
import scanpy as sc
import base64
from io import BytesIO
import matplotlib.pyplot as plt

router = APIRouter(prefix="/visualize", tags=["visualize"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/umap/{dataset_id}")
def get_umap_plot(dataset_id: int, db: Session = Depends(get_db)):
    ds = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not ds or ds.processed == 0:
        raise HTTPException(status_code=404, detail="Processed dataset not found")
    processed_path = f"data/uploads/processed_{ds.filename}.h5ad"
    if not os.path.exists(processed_path):
        raise HTTPException(status_code=404, detail="Processed file not found")
    adata = sc.read_h5ad(processed_path)

    fig = sc.pl.umap(adata, show=False)
    buf = BytesIO()
    fig.figure.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig.figure)
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode("utf-8")
    return {"image_base64": img_b64}
