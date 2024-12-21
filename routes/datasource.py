"""
contains mappings for datasources api
:author Muhammad Rowaha<ashfaqrowaha@gmail.com>
"""
import io
from fastapi import APIRouter, UploadFile, File, Form, FastAPI, Depends
from persistence.injectors import getBlobStorage, IBlobPersistence
router = APIRouter(prefix="/datasource")


@router.post("/upload")
async def uploadFile(
    datasource: str = Form(...),
    file: UploadFile = File(...),
    blobPersistence: IBlobPersistence = Depends(getBlobStorage)
):
    blobPersistence.createBucket("hello")

    # extract file information
    fileContent = await file.read()
    fileSize = len(fileContent)
    blobPersistence.uploadFile(
        file.filename,
        bucket="hello",
        size=fileSize,
        data=io.BytesIO(fileContent),
        type=file.content_type
    )

    return {
        "ok": True
    }


def register(app: FastAPI, *, prefix=str) -> None:
    global router
    app.include_router(router, prefix=prefix)
