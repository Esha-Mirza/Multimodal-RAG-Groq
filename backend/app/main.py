
from fastapi import FastAPI

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
    return {
        "status": "healthy"
    }
