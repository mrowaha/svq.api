from pydantic import BaseModel


class CreateDatasource(BaseModel):
    name: str


class CreateDatasourceRes(BaseModel):
    name: str
    id: int


class DeleteDatasource(BaseModel):
    id: int
