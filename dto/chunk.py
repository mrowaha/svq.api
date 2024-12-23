from pydantic import BaseModel


class Chunk(BaseModel):
    content: str
    pages: list[int]
