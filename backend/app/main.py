
from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.api.upload import router as upload_router


app = FastAPI(
    title="Multimodal RAG API",
    description="A Multimodal RAG system powered by Groq and ChromaDB",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to Multimodal RAG!",
        "status": "Backend is running"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


app.include_router(chat_router)
app.include_router(upload_router)
