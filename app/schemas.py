from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DatasetCreate(BaseModel):
    name: str
    metadata: Optional[str] = None

class DatasetOut(BaseModel):
    id: int
    name: str
    filename: str
    file_type: str
    metadata: Optional[str]
    uploaded_at: datetime
    processed: int

    class Config:
        orm_mode = True
