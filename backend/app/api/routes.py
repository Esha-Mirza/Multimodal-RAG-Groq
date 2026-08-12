

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from app.services.groq_client import groq_client

router = APIRouter(prefix="/api/v1", tags=["api"])

documents: Dict[str, Any] = {}

class TestGroqRequest(BaseModel):
 
    prompt: Optional[str] = None

class TestGroqResponse(BaseModel):

    success: bool
    message: str
    response: Optional[str] = None
    error: Optional[str] = None
    model: Optional[str] = None

@router.get("/health")
async def api_health_check():

    return {
        "status": "healthy",
        "service": "Multi-RAG API",
        "document_count": len(documents)
    }

@router.get("/info")
async def get_info():

    return {
        "name": "Multi-RAG Application with Groq",
        "version": "1.0.0",
        "status": "running",
        "documents_loaded": len(documents),
        "endpoints": {
            "upload": "/api/v1/upload",
            "ask": "/api/v1/ask",
            "documents": "/api/v1/documents",
            "health": "/api/v1/health",
            "test-groq": "/api/v1/test-groq (POST)",
            "test-groq-get": "/api/v1/test-groq (GET) - for browser testing"
        }
    }

@router.get("/test-groq")
async def test_groq_get(
    prompt: Optional[str] = Query(None, description="The prompt to send to Groq")
):
 
    try:
        if prompt:
            result = groq_client.generate_response(
                prompt=prompt,
                max_tokens=200
            )
        else:
            result = groq_client.test_connection()
        
        if result["success"]:
            return {
                "success": True,
                "message": "Groq API test successful!",
                "response": result.get("response"),
                "model": result.get("model")
            }
        else:
            return {
                "success": False,
                "message": "Groq API test failed",
                "error": result.get("error")
            }
    except Exception as e:
        return {
            "success": False,
            "message": "Error testing Groq API",
            "error": str(e)
        }

@router.post("/test-groq", response_model=TestGroqResponse)
async def test_groq_post(request: TestGroqRequest = None):

    try:
        if request and request.prompt:
            # Use custom prompt
            result = groq_client.generate_response(
                prompt=request.prompt,
                max_tokens=200
            )
        else:
            # Use default test
            result = groq_client.test_connection()
        
        if result["success"]:
            return TestGroqResponse(
                success=True,
                message="Groq API test successful!",
                response=result.get("response"),
                model=result.get("model")
            )
        else:
            return TestGroqResponse(
                success=False,
                message="Groq API test failed",
                error=result.get("error")
            )
            
    except Exception as e:
        return TestGroqResponse(
            success=False,
            message="Error testing Groq API",
            error=str(e)
        )

@router.post("/upload")
async def upload_document():

    return {"message": "Document upload will be implemented in Phase 6"}

@router.post("/ask")
async def ask_question():

    return {"message": "Question answering will be implemented in Phase 9"}

@router.get("/documents")
async def get_documents():

    return {"documents": list(documents.keys())}

@router.delete("/documents/{doc_id}")
async def delete_document(doc_id: str):

    return {"message": f"Document {doc_id} deletion will be implemented later"}