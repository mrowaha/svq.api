"""
this route is an echo endpoint that returns whatever you send it
:author Muhammad Rowaha<ashfaqrowaha@gmail.com>
"""
from dto.echo import EchoMessageReq, EchoMessageResponse
from fastapi import APIRouter, FastAPI
from typing import Union
router = APIRouter()


@router.post('/echo')
async def echo(req: EchoMessageReq) -> EchoMessageResponse:
    """
    Endpoint to echo back the received message.
    :param msg: JSON object with a "message" field
    :return: JSON object with the same "message"
    """
    return EchoMessageResponse(message=f"echo: {req.message}")


def register(app: FastAPI, *, prefix=str) -> None:
    global router
    app.include_router(router, prefix=prefix)
