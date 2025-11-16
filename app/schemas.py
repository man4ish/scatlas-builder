"""
Pydantic schemas for Single-Cell Atlas Builder.

Defines request and response models for the API. Used for validation and serialization
of Dataset objects when interacting with FastAPI endpoints.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DatasetCreate(BaseModel):
    """
    Schema for creating a new dataset.

    Attributes:
        name (str): Name of the dataset (required).
        meta_info (Optional[str]): Optional metadata or description.
    """
    name: str
    meta_info: Optional[str] = None

class DatasetOut(BaseModel):
    """
    Schema for returning dataset details in API responses.

    Attributes:
        id (int): Dataset ID.
        name (str): Name of the dataset.
        filename (str): Stored filename on disk.
        file_type (str): File type/extension (e.g., h5ad, csv).
        meta_info (Optional[str]): Optional metadata or description.
        uploaded_at (datetime): Timestamp when uploaded.
        processed (int): 0 = not processed, 1 = processed.
        processed_file (Optional[str]): Path to processed file if available.
    """
    id: int
    name: str
    filename: str
    file_type: str
    meta_info: Optional[str] = None
    uploaded_at: datetime
    processed: int = 0
    processed_file: Optional[str] = None

    class Config:
        """
        Pydantic configuration to allow loading data from ORM objects.
        """
        from_attributes = True
