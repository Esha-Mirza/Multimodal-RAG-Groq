

import json
import os
from typing import List

from dotenv import load_dotenv
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


load_dotenv()

class Settings(BaseSettings):
   
    
   
    groq_api_key: str = Field(..., env="GROQ_API_KEY")
    
   
    backend_host: str = Field("0.0.0.0", env="BACKEND_HOST")
    backend_port: int = Field(8000, env="BACKEND_PORT")
    
  
    chroma_db_path: str = Field("./chroma_db", env="CHROMA_DB_PATH")
    
    
    max_upload_size: int = Field(10485760, env="MAX_UPLOAD_SIZE")
    

    allowed_origins: str = Field(
        "http://localhost:5173,http://localhost:3000",
        env="ALLOWED_ORIGINS"
    )
    
   
    allowed_extensions: List[str] = [".pdf", ".txt", ".docx"]
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    
    class Config:
        """Pydantic v2 configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
       
        extra = "ignore"
    
    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_allowed_origins(cls, v):
       
        if isinstance(v, str):
            try:
        
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return v  
            except json.JSONDecodeError:
                pass
     
            return v
        return v
    
    def get_allowed_origins_list(self) -> List[str]:

        raw = self.allowed_origins.strip()
        if not raw:
            return ["http://localhost:5173"]
        
        try:
            # Try parsing as JSON
            parsed = json.loads(raw)
            if isinstance(parsed, list):
                return [str(item) for item in parsed if item]
        except json.JSONDecodeError:
            pass
        

        return [origin.strip() for origin in raw.split(",") if origin.strip()]


settings = Settings()


if not settings.groq_api_key or settings.groq_api_key == "your_groq_api_key_here":
    print("⚠️  WARNING: GROQ_API_KEY not set or using placeholder!")
    print("   Please set your Groq API key in backend/.env file")
    print(f"   Current value: {settings.groq_api_key[:10]}...")