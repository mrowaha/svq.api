from pydantic import BaseModel


class RegisterDto(BaseModel):
    username: str
    password: str
    firstname: str
    lastname: str
    email: str


class RegisterRespDto(BaseModel):
    userId: str
