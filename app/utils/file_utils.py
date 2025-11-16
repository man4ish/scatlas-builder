"""
Utility functions for file handling in Single-Cell Atlas Builder.

This module provides helper functions to save uploaded files with unique filenames 
and manage the upload directory structure. It ensures reproducibility and prevents
filename collisions by generating UUID-based filenames.
"""

import os
from uuid import uuid4
from fastapi import UploadFile

# Default directory to store uploaded datasets
DEFAULT_UPLOAD_DIR = "data/uploads"
os.makedirs(DEFAULT_UPLOAD_DIR, exist_ok=True)

async def save_uploaded_file(file: UploadFile, upload_dir: str = DEFAULT_UPLOAD_DIR):
    """
    Save an uploaded file to the specified directory with a unique UUID-based filename.

    Args:
        file (UploadFile): The uploaded file object received via FastAPI.
        upload_dir (str): The target directory to save the file. Defaults to DEFAULT_UPLOAD_DIR.

    Returns:
        tuple: (unique_filename, full_file_path)
            - unique_filename: The generated filename with UUID and original extension.
            - full_file_path: Complete path where the file is saved.
    
    Raises:
        OSError: If the file cannot be written to the target directory.
    """
    # Ensure the upload directory exists
    os.makedirs(upload_dir, exist_ok=True)

    # Extract file extension
    ext = file.filename.split(".")[-1].lower()

    # Generate unique filename to prevent collisions
    unique_name = f"{uuid4().hex}.{ext}"
    file_path = os.path.join(upload_dir, unique_name)

    # Read the file content asynchronously
    content = await file.read()

    # Save the content to disk
    with open(file_path, "wb") as f:
        f.write(content)

    return unique_name, file_path
