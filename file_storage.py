import os
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile

UPLOAD_ROOT = Path(os.environ.get("UPLOAD_DIR", "uploads"))

ALLOWED_EXTENSIONS = {
    # documents
    ".pdf", ".doc", ".docx", ".txt", ".zip",
    # code
    ".py", ".ipynb", ".c", ".cpp", ".java", ".js",
    # images
    ".jpg", ".jpeg", ".png", ".gif", ".webp",
}

MAX_FILE_SIZE_BYTES = 20 * 1024 * 1024  # 20 MB


def save_upload(upload: UploadFile, subfolder: str) -> tuple[str, str]:
    """
    Saves an uploaded file to disk under UPLOAD_ROOT/subfolder with a
    random name (to avoid collisions/overwrites), keeping the original
    extension.

    Returns (relative_path, original_filename) — both get stored in the DB.
    relative_path is what you append to "/uploads/" to download the file.
    """
    original_name = upload.filename or "file"
    ext = Path(original_name).suffix.lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type '{ext}' is not allowed. Allowed types: {', '.join(sorted(ALLOWED_EXTENSIONS))}",
        )

    folder = UPLOAD_ROOT / subfolder
    folder.mkdir(parents=True, exist_ok=True)

    stored_name = f"{uuid.uuid4().hex}{ext}"
    stored_path = folder / stored_name

    contents = upload.file.read(MAX_FILE_SIZE_BYTES + 1)
    if len(contents) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(status_code=400, detail="File is too large (max 20MB)")

    with open(stored_path, "wb") as f:
        f.write(contents)

    relative_path = f"{subfolder}/{stored_name}"
    return relative_path, original_name