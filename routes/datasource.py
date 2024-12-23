"""
contains mappings for datasources api
:author Muhammad Rowaha<ashfaqrowaha@gmail.com>
"""
import io
from fastapi import APIRouter, UploadFile, File, Form, FastAPI, Depends
from persistence.injectors import getBlobStorage, IBlobPersistence
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from fastapi.responses import Response

router = APIRouter(prefix="/datasource")


@router.post("/upload")
async def uploadFile(
    datasource: str = Form(...),
    file: UploadFile = File(...),
    enable_ocr: Optional[bool] = Form(False),  # New parameter
    extract_tables: Optional[bool] = Form(False),  # New parameter
    blobPersistence: IBlobPersistence = Depends(getBlobStorage)
):
    # Validate file type
    allowed_types = ["application/pdf",
                     "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain"]
    if file.content_type not in allowed_types:
        return {
            "ok": False,
            "error": "Unsupported file type. Only PDF, DOCX, and TXT files are allowed."
        }

    try:
        # Create a unique bucket name based on datasource type
        bucket_name = f"docs-{datasource}"
        blobPersistence.createBucket(bucket_name)

        # Extract file information
        fileContent = await file.read()
        fileSize = len(fileContent)

        # Add metadata about processing options
        metadata = {
            "enable_ocr": str(enable_ocr).lower(),
            "extract_tables": str(extract_tables).lower(),
            "original_filename": file.filename,
            "content_type": file.content_type
        }

        blobPersistence.uploadFile(
            file.filename,
            bucket=bucket_name,
            size=fileSize,
            data=io.BytesIO(fileContent),
            type=file.content_type,
            # You'll need to add metadata support to your MinioPersistence class
            metadata=metadata
        )

        return {
            "ok": True,
            "filename": file.filename,
            "size": fileSize,
            "processing_options": {
                "ocr_enabled": enable_ocr,
                "table_extraction_enabled": extract_tables
            }
        }
    except Exception as e:
        return {
            "ok": False,
            "error": str(e)
        }

class Document(BaseModel):
    name: str
    size: int
    lastModified: str
    contentType: str = ""
    originalFilename: str

class ListDocumentsResponse(BaseModel):
    ok: bool
    documents: List[Document]
    error: str | None = None

@router.get("/list", response_model=ListDocumentsResponse)
async def listDocuments(
    datasource: str,
    blobPersistence: IBlobPersistence = Depends(getBlobStorage)
) -> ListDocumentsResponse:
    try:
        bucket_name = f"docs-{datasource}"
        objects = blobPersistence.listObjects(bucket_name)
        
        documents = []
        for obj in objects:
            # Extract metadata if available
            metadata = obj.metadata if hasattr(obj, 'metadata') else {}
            
            documents.append(Document(
                name=obj.object_name,
                size=obj.size,
                lastModified=obj.last_modified.isoformat() if hasattr(obj, 'last_modified') else datetime.now().isoformat(),
                contentType=metadata.get("content_type", ""),
                originalFilename=metadata.get("original_filename", obj.object_name)
            ))
            
        return ListDocumentsResponse(ok=True, documents=documents)
    except Exception as e:
        return ListDocumentsResponse(ok=False, documents=[], error=str(e))

@router.get("/content/{name}")
async def getDocumentContent(
    name: str,
    datasource: str,
    blobPersistence: IBlobPersistence = Depends(getBlobStorage)
) -> Response:
    try:
        bucket_name = f"docs-{datasource}"
        data = blobPersistence.getObject(bucket_name, name)
        return Response(
            content=data,
            media_type="application/pdf"
        )
    except Exception as e:
        return {
            "ok": False,
            "error": str(e)
        }

def register(app: FastAPI, *, prefix: str) -> None:
    global router
    app.include_router(router, prefix=prefix)