
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class DocumentUploadResponse(BaseModel):
    success: bool
    document_id: str
    filename: str
    message: str
    chunk_count: int = 0

class QuestionRequest(BaseModel):
    question: str = Field(..., description="The user's question")
    max_chunks: int = Field(5, description="Maximum number of chunks to retrieve")
    temperature: float = Field(0.7, description="Temperature for LLM generation")

class SourceChunk(BaseModel):
    document_id: str
    document_name: str
    chunk_text: str
    relevance_score: float

class QuestionResponse(BaseModel):
    answer: str
    sources: List[SourceChunk]
    question: str

class DocumentInfo(BaseModel):
    document_id: str
    filename: str
    uploaded_at: str
    chunk_count: int

class DeleteResponse(BaseModel):
    success: bool
    message: str