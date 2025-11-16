"""
Main entrypoint for the Single-Cell Atlas Builder FastAPI application.

This module initializes the FastAPI app, creates database tables, and includes
the routers for dataset upload, preprocessing/integration, and visualization.

Routers:
    - upload: Handles dataset uploads
    - integrate: Runs preprocessing, QC, normalization, PCA, UMAP, and clustering
    - visualize: Provides UMAP visualization endpoints
"""

from fastapi import FastAPI
from app.database import Base, engine
from app.routers import upload, integrate, visualize

# Create all database tables if they do not exist
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Single-Cell Atlas Builder", version="0.1.0")

# Include routers
app.include_router(upload.router)
app.include_router(integrate.router)
app.include_router(visualize.router)


@app.get("/")
def root():
    """
    Root endpoint to verify that the API is running.

    Returns:
        dict: Simple JSON message confirming the API status
    """
    return {"message": "Single-Cell Atlas Builder API is running"}
