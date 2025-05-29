"""
UK Probate/Divorce AI Agent - Main Application
This is the heart of our backend server
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from dotenv import load_dotenv

# Load our secret keys from .env file
load_dotenv(dotenv_path="../.env")

# Import our custom code
from app.api.v1.api import api_router
from app.core.config import settings

# Create our web application
app = FastAPI(
    title="UK Probate/Divorce AI Agent",
    version="1.0.0",
    description="AI helpers for UK legal cases",
    docs_url="/docs"  # This creates automatic documentation
)

# Allow our frontend to talk to our backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect our API routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def home():
    """This is what people see when they visit our website"""
    return {
        "message": "🏠 UK Probate/Divorce AI Agent is running!",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.get("/health")
async def health_check():
    """Check if everything is working"""
    return {
        "status": "✅ All systems operational",
        "ai_agents": "🤖 Ready to help",
        "database": "💾 Connected"
    }

# This runs our server when we start the file
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Automatically restart when we change code
    )