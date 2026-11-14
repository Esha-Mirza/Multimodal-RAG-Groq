
from fastapi import APIRouter
from app.schemas.chat import ChatRequest
from app.services.rag_service import ask_question


router = APIRouter()


@router.post("/ask")
def ask(request: ChatRequest):

    result = ask_question(
        question=request.question,
        n_results=request.n_results)

    return result
