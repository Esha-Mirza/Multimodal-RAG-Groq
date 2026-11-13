from groq import Groq
from app.core.config import GROQ_API_KEY

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing from .env file")

client = Groq(api_key=GROQ_API_KEY)