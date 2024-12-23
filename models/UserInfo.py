from pydantic import BaseModel
from typing import Optional


class UserInfo(BaseModel):
    username: str
    email: Optional[str] = None
    fullname: Optional[str] = None
