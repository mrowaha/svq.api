from pydantic import BaseModel


class EchoMessageReq(BaseModel):
    message: str


class EchoMessageResponse(EchoMessageReq):
    pass
