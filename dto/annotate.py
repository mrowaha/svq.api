from pydantic import BaseModel
from typing import List
from .chunk import Chunk


class Annotate(BaseModel):
    datasource: str
    filename: str
    chunks: List[Chunk]
