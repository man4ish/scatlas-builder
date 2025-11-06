from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from .database import Base

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    meta_info = Column(Text, nullable=True)  # <- renamed from 'metadata'
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    processed = Column(Integer, default=0, nullable=False)
    processed_file = Column(String, nullable=True)

    def __repr__(self):
        return f"<Dataset(id={self.id}, name={self.name}, processed={self.processed})>"
