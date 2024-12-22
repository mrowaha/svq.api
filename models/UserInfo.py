from pydantic import BaseModel
from typing import Optional


class UserInfo(BaseModel):
    preferred_username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
