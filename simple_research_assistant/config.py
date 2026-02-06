"""
Simplified Configuration - Only GPT-4o, No Fallbacks
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Simple configuration for Azure OpenAI GPT-4o only"""
    
    # Azure OpenAI - Only one model, no fallbacks
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
    AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")
    
    # Server
    BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8000"))
    FRONTEND_PORT = int(os.getenv("FRONTEND_PORT", "8501"))
    
    # PubMed
    PUBMED_EMAIL = os.getenv("PUBMED_EMAIL", "researcher@example.com")
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./research.db")
    
    @classmethod
    def validate(cls):
        """Validate required settings"""
        if not all([cls.AZURE_OPENAI_ENDPOINT, cls.AZURE_OPENAI_API_KEY]):
            raise ValueError("AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY are required!")
        return True


# Global config
config = Config()
