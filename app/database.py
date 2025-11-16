"""
Database setup for Single-Cell Atlas Builder.

This module configures the SQLAlchemy engine, session, and declarative base
for interacting with the SQLite database that stores dataset metadata and processing status.

Database URL:
- Using SQLite: `scatlas.db` in the project directory.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./scatlas.db"

# Create SQLAlchemy engine
# connect_args={"check_same_thread": False} is required for SQLite to allow usage across threads
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create session factory for database interactions
SessionLocal = sessionmaker(
    autocommit=False,  # changes are committed explicitly
    autoflush=False,   # flush is done manually
    bind=engine
)

# Base class for ORM models
Base = declarative_base()
