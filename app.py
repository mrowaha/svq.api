from fastapi import FastAPI
from routes import registerDataSourceHandlers
app = FastAPI(
    docs_url="/docs",
    description="SVQ backend api",
)
registerDataSourceHandlers(app, prefix="/v1")
