
from pathlib import Path
from uuid import uuid4
import traceback

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.document_service import (
    ingest_text_document,
    ingest_pdf_document,
    ingest_docx_document
)


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

UPLOAD_DIR = Path(__file__).resolve().parents[2] / "data" / "uploads"

MAX_FILE_SIZE = 25 * 1024 * 1024


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No filename provided."
        )

    original_filename = Path(
        file.filename.replace("\\", "/")
    ).name

    file_extension = Path(original_filename).suffix.lower()

    if file_extension not in [".txt", ".pdf", ".docx"]:
        raise HTTPException(
            status_code=400,
            detail="Supported formats are .txt, .pdf, and .docx."
        )

    file_content = await file.read(MAX_FILE_SIZE + 1)

    if not file_content:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty."
        )

    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size must not exceed 25 MB."
        )

    unique_filename = f"{uuid4().hex}_{original_filename}"

    UPLOAD_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    file_path = UPLOAD_DIR / unique_filename

    try:

        file_path.write_bytes(file_content)

        if file_extension == ".txt":

            try:
                text = file_content.decode("utf-8")
            except UnicodeDecodeError:
                raise HTTPException(
                    status_code=400,
                    detail="The file must use UTF-8 encoding."
                )

            if not text.strip():
                raise HTTPException(
                    status_code=400,
                    detail="The document contains no readable text."
                )

            result = ingest_text_document(
                text=text,
                source=unique_filename
            )

        elif file_extension == ".pdf":

            result = ingest_pdf_document(
                file_path=file_path,
                source=unique_filename
            )

        else:

            result = ingest_docx_document(
                file_path=file_path,
                source=unique_filename
            )

    except HTTPException:

        if file_path.exists():
            file_path.unlink()

        raise

    except (ValueError, FileNotFoundError) as error:

        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:

        traceback.print_exc()

        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=500,
            detail="Document processing failed. Check the backend terminal."
        )

    response = {
        "message": "Document uploaded and processed successfully.",
        "filename": original_filename,
        "total_chunks": result["total_chunks"],
        "stored_chunks": result["stored_chunks"]
    }

    if file_extension == ".pdf":

        response["total_pages"] = result["total_pages"]
        response["total_images"] = result["total_images"]

    elif file_extension == ".docx":

        response["total_text_blocks"] = result["total_text_blocks"]
        response["total_content_blocks"] = result["total_content_blocks"]
        response["total_images"] = result["total_images"]
        response["images_processed"] = result["images_processed"]
        response["images_skipped"] = result["images_skipped"]
        response["skipped_images"] = result["skipped_images"]

    return response
