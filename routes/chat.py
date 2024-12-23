from fastapi import APIRouter, FastAPI, Depends
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

router = APIRouter(prefix="/chat")

class Message(BaseModel):
    id: str
    content: str
    timestamp: datetime
    role: str  # 'user' or 'assistant'
    documentId: Optional[str] = None

class ChatRequest(BaseModel):
    message: str
    documentId: Optional[str] = None

class ChatResponse(BaseModel):
    ok: bool
    message: Message
    error: Optional[str] = None

@router.post("/send", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    try:
        # For now, just echoing the message
        response_message = Message(
            id=str(datetime.now().timestamp()),
            content=f"We have received your message about document {request.documentId}: {request.message}",
            timestamp=datetime.now(),
            role="assistant",
            documentId=request.documentId
        )
        
        return ChatResponse(ok=True, message=response_message)
    except Exception as e:
        return ChatResponse(ok=False, error=str(e))

@router.get("/history/{document_id}", response_model=List[Message])
async def get_chat_history(document_id: str):
    # For now, returning an empty list
    return []

def register(app: FastAPI, *, prefix=str) -> None:
    global router
    app.include_router(router, prefix=prefix)