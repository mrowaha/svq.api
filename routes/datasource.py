"""
contains mappings for datasources api
:author Muhammad Rowaha<ashfaqrowaha@gmail.com>
"""
import asyncio
from fastapi import APIRouter, UploadFile, File, Form, FastAPI, Depends, status, HTTPException, WebSocket, WebSocketDisconnect
from typing import Optional, List
from service.datasource import DatasourceService, get_datasource_service
from service.datasource.exceptions import UnsupportedFileType, DatasourceNotFoundError
from dto.datasource import CreateDatasource, CreateDatasourceRes, DeleteDatasource
from persistence.injectors import getBlobStorage, IBlobPersistence
from datetime import datetime
from pydantic import BaseModel
from fastapi.responses import Response

router = APIRouter(prefix="/datasource")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CreateDatasourceRes)
async def create_datasource(
    req: CreateDatasource,
    datasource_service: DatasourceService = Depends(get_datasource_service)
):
    id = datasource_service.create_datasource(req.name)
    return CreateDatasourceRes(
        id=id,
        name=req.name
    )


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_datasource(
    req: DeleteDatasource,
    datasource_service: DatasourceService = Depends(get_datasource_service)
):
    try:
        datasource_service.delete_datasource(req.id)
    except DatasourceNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="does not exist"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="unknown error"
        )


# Timeout in seconds for idle connection on a chat socket
IDLE_CHAT_TIMEOUT = 120


@router.websocket("/chat/{datasource_id}")
async def datasource_chat(websocket: WebSocket, datasource_id: int):
    await websocket.accept()
    print(f"WebSocket connection accepted {datasource_id}")
    message = await websocket.receive_text()
    print(f"Received: {message}")
    answer = f"You asked: '{message}'. Here's your answer!"
    await websocket.send_text(answer)

    # try:
    #     while True:
    #         try:
    #             # message = await asyncio.wait_for(websocket.receive_text(), timeout=IDLE_CHAT_TIMEOUT)
    #             last_activity_time = asyncio.get_event_loop().time()
    #             message = await websocket.receive_text()
    #             print(f"Received: {message}")
    #             answer = f"You asked: '{message}'. Here's your answer!"
    #             await websocket.send_text(answer)
    #         except asyncio.TimeoutError:
    #             current_time = asyncio.get_event_loop().time()
    #             if current_time - last_activity_time > IDLE_CHAT_TIMEOUT:
    #                 print("Closing connection due to idle timeout")
    #                 await websocket.close()
    #                 break
    # except WebSocketDisconnect:
    #     print("Client disconnected")
    # except Exception as e:
    #     print(f"Error: {e}")
    #     await websocket.close()


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def uploadFile(
    datasource: str = Form(...),
    file: UploadFile = File(...),
    enable_ocr: Optional[bool] = Form(False),  # New parameter
    extract_tables: Optional[bool] = Form(False),  # New parameter
    datasource_service: DatasourceService = Depends(get_datasource_service)
):
    try:
        content = await file.read()
        datasource_service.upload_file(
            datasource,
            file.filename,
            content,
            extract_tables=extract_tables,
            enable_ocr=enable_ocr,
            content_type=file.content_type
        )
    except UnsupportedFileType:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="unsupported file extension"
        )


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
                lastModified=obj.last_modified.isoformat() if hasattr(
                    obj, 'last_modified') else datetime.now().isoformat(),
                contentType=metadata.get("content_type", ""),
                originalFilename=metadata.get(
                    "original_filename", obj.object_name)
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
