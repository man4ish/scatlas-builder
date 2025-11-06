from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DatasetCreate(BaseModel):
    name: str
    meta_info: Optional[str] = None

class DatasetOut(BaseModel):
    id: int
    name: str
    filename: str
    file_type: str
    meta_info: Optional[str] = None
    uploaded_at: datetime
    processed: int = 0
    processed_file: Optional[str] = None

    class Config:
        from_attributes = True
