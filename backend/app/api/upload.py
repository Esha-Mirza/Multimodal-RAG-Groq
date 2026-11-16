
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.document_service import ingest_text_document


router = APIRouter(prefix="/documents",
    tags=["Documents"])

UPLOAD_DIR = Path(__file__).resolve().parents[2] / "data" / "uploads"

MAX_FILE_SIZE = 5 * 1024 * 1024


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    if not file.filename:
        raise HTTPException(status_code=400,
            detail="No filename provided.")

    original_filename = Path(file.filename.replace("\\", "/")).name

    if Path(original_filename).suffix.lower() != ".txt":
        raise HTTPException(status_code=400,
            detail="Only .txt files are supported currently.")

    file_content = await file.read(MAX_FILE_SIZE + 1)

    if not file_content:
        raise HTTPException(status_code=400,
            detail="The uploaded file is empty.")

    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413,
            detail="File size must not exceed 5 MB.")

    try:
        text = file_content.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400,
            detail="The file must use UTF-8 encoding.")

    if not text.strip():
        raise HTTPException(status_code=400,
            detail="The document contains no readable text.")

    # Generate a unique filename to avoid overwriting files
    unique_filename = f"{uuid4().hex}_{original_filename}"

    UPLOAD_DIR.mkdir(parents=True,exist_ok=True)

    file_path = UPLOAD_DIR / unique_filename

    try:
        file_path.write_bytes(file_content)

        result = ingest_text_document(text=text,source=unique_filename)

    except Exception:
        if file_path.exists():
            file_path.unlink()

        raise HTTPException(status_code=500,
            detail="Document processing failed.")

    return {
        "message": "Document uploaded and processed successfully.",
        "filename": original_filename,
        "total_chunks": result["total_chunks"],
        "stored_chunks": result["stored_chunks"]}
