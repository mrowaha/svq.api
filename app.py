from fastapi import FastAPI
from routes import register_echo
app = FastAPI(
    docs_url="/docs",
    description="SVQ backend api",
)
register_echo(app, prefix="/v1")
