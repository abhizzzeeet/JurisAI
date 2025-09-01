from fastapi import APIRouter
from pydantic import BaseModel
from app.chat_engine import get_response

router = APIRouter()

class QueryInput(BaseModel):
    query: str

@router.post("/chat")
async def chat_endpoint(data: QueryInput):
    result = get_response(data.query)
    return {"response": result}