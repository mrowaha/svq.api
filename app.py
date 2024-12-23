from dotenv import load_dotenv
from fastapi import FastAPI
from routes import registerDataSourceHandlers, registerEcho, registerAuth, chat

load_dotenv()
app = FastAPI(
    docs_url="/docs",
    description="SVQ backend api",
)

registerAuth(app, prefix="/v1")
registerDataSourceHandlers(app, prefix="/v1")
chat.register(app, prefix="/v1")
registerEcho(app, prefix="/v1")