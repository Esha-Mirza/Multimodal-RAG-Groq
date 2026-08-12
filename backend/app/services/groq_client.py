"""Groq API client for LLM interactions."""

import os
from typing import Optional, Dict, Any, List

from groq import Groq
from app.config import settings

class GroqClient:
    """Client for interacting with Groq's API."""
    
    def __init__(self):
        """Initialize the Groq client with API key from settings."""
        self.api_key = settings.groq_api_key
        if not self.api_key or self.api_key == "your_groq_api_key_here":
            raise ValueError(
                "GROQ_API_KEY is not set. Please add it to your .env file."
            )
        
        # Initialize the Groq client
        self.client = Groq(api_key=self.api_key)
        
        # Updated to use active model
        # You can change this to any active model from the list above
        self.default_model = "llama-3.3-70b-versatile"
    
    def test_connection(self) -> Dict[str, Any]:
        """Test the connection to Groq API with a simple prompt."""
        try:
            # Send a simple test prompt
            response = self.client.chat.completions.create(
                model=self.default_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant. Respond with 'OK' if you can hear me."
                    },
                    {
                        "role": "user",
                        "content": "Can you hear me? Just say 'OK'."
                    }
                ],
                max_tokens=10,
                temperature=0.0,
            )
            
            # Extract the response content
            content = response.choices[0].message.content
            
            return {
                "success": True,
                "message": "Groq API connection successful!",
                "response": content,
                "model": self.default_model
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to connect to Groq API"
            }
    
    def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 500,
        temperature: float = 0.7,
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a response from Groq based on the prompt.
        
        Args:
            prompt: The user's question or prompt
            system_prompt: Optional system instructions
            max_tokens: Maximum tokens in response
            temperature: Randomness (0.0 to 1.0)
            model: Model to use (defaults to llama-3.3-70b-versatile)
        """
        try:
            # Prepare messages
            messages = []
            
            # Add system prompt if provided
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            # Add user message
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            # Use provided model or default
            model_to_use = model or self.default_model
            
            # Send request to Groq
            response = self.client.chat.completions.create(
                model=model_to_use,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            
            # Extract the response
            content = response.choices[0].message.content
            
            return {
                "success": True,
                "response": content,
                "model": model_to_use,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to generate response from Groq"
            }

# Create a singleton instance
groq_client = GroqClient()