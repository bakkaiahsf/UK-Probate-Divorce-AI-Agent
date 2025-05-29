"""
Configuration settings for our application
This file manages all our settings and secret keys
"""

from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """All the settings our app needs"""
    
    # Basic app info
    APP_NAME: str = "UK Probate/Divorce AI Agent"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Database (we're using simple SQLite for now)
    DATABASE_URL: str = "sqlite:///./uk_probate.db"
    
    # AI settings
    OPENAI_API_KEY: str = "your-key-here"
    OPENAI_MODEL: str = "gpt-4o-mini"
    SERPER_API_KEY: str = "your-serper-key-here"
    
    # Security
    SECRET_KEY: str = "change-this-in-production"
    
    # Frontend connection
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    class Config:
        env_file = "../.env"  # Look for .env file in parent directory
        case_sensitive = True

# Create one instance of settings for the whole app
settings = Settings()