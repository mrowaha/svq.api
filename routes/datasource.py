"""
contains mappings for datasources api
:author Muhammad Rowaha<ashfaqrowaha@gmail.com>
"""
from fastapi import APIRouter, UploadFile, File, Form, FastAPI
router = APIRouter(prefix="/datasource")


@router.post("/upload")
async def uploadFile(
    datasource: str = Form(...),
    content: UploadFile = File(...)
):

    print(f"uploading datasource for file {datasource}")
    blob = await content.read()

    print(f"file content {blob}")
    return {
        "ok": True
    }


def register(app: FastAPI, *, prefix=str) -> None:
    global router
    app.include_router(router, prefix=prefix)
