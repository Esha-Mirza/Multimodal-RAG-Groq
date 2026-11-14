
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(min_length=1)
    n_results: int = Field(default=3, ge=1, le=10)
