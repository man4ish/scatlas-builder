"""
ORM models for Single-Cell Atlas Builder.

Defines the database tables using SQLAlchemy ORM. Currently, it includes the Dataset model
to track uploaded datasets, processing status, and associated metadata.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from .database import Base

class Dataset(Base):
    """
    Represents a single dataset uploaded to the Single-Cell Atlas Builder.

    Attributes:
        id (int): Primary key.
        name (str): Name of the dataset.
        filename (str): Stored filename on disk.
        file_type (str): File extension/type (e.g., h5ad, csv).
        meta_info (str): Optional metadata provided by user.
        uploaded_at (datetime): Timestamp when uploaded.
        processed (int): 0 = not processed, 1 = processed.
        processed_file (str): Path to the processed h5ad file.
    """
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    meta_info = Column(Text, nullable=True)  # renamed from 'metadata' to avoid conflict
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    processed = Column(Integer, default=0, nullable=False)
    processed_file = Column(String, nullable=True)

    def __repr__(self):
        """
        Returns a readable string representation of the Dataset object.
        """
        return f"<Dataset(id={self.id}, name={self.name}, processed={self.processed})>"
