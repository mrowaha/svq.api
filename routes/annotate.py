"""
an unprotected route that annotates pdf based on chunk requests
"""
from fastapi import APIRouter, Depends, FastAPI, Response, status
from dto.annotate import Annotate
from persistence.blob import IBlobPersistence
from persistence.injectors import getBlobStorage
from domain.annotator import Annotator, get_annotator
router = APIRouter(prefix="/annotate")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def annotate(
    req: Annotate,
    blobPersistence: IBlobPersistence = Depends(getBlobStorage),
    annotator: Annotator = Depends(get_annotator)
):
    annotated_data = annotator.annotate(req.chunks, blobPersistence,
                                        bucket_name=req.datasource, file_name=req.filename)
    return Response(content=annotated_data, media_type='application/pdf')


def register(app: FastAPI, *, prefix: str) -> None:
    global router
    app.include_router(router, prefix=prefix)
