

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes
from app.config import settings


app = FastAPI(
    title="Multi-RAG Application with Groq",
    description="A Multi-RAG system with document upload, vector search, and Groq API integration",
    version="1.0.0"
)

allowed_origins = settings.get_allowed_origins_list()

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(routes.router)

@app.get("/health")
async def health_check():

    return {
        "status": "healthy",
        "message": "Multi-RAG backend is running!",
        "version": "1.0.0"
    }

# Root endpoint
@app.get("/")
async def root():
    return {
        "name": "Multi-RAG Application with Groq",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=True
    )