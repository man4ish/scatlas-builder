import os
from uuid import uuid4
from fastapi import UploadFile

DEFAULT_UPLOAD_DIR = "data/uploads"
os.makedirs(DEFAULT_UPLOAD_DIR, exist_ok=True)

async def save_uploaded_file(file: UploadFile, upload_dir: str = DEFAULT_UPLOAD_DIR):
    os.makedirs(upload_dir, exist_ok=True)
    ext = file.filename.split(".")[-1].lower()
    unique_name = f"{uuid4().hex}.{ext}"
    file_path = os.path.join(upload_dir, unique_name)

    content = await file.read()  # only await UploadFile.read()
    with open(file_path, "wb") as f:
        f.write(content)

    return unique_name, file_path
