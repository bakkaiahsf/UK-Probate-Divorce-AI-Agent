"""
Main API router - This connects all our endpoints
"""

from fastapi import FastAPI, APIRouter
from app.api.v1.endpoints import cases

# Create the main router
api_router = APIRouter()

# Add our case endpoints
api_router.include_router(cases.router, prefix="/cases", tags=["cases"])

@api_router.get("/")
async def api_info():
    """Information about our API"""
    return {
        "message": "🤖 UK Probate/Divorce AI Agent API",
        "version": "1.0.0",
        "available_endpoints": {
            "create_probate_case": "POST /cases/probate",
            "create_divorce_case": "POST /cases/divorce", 
            "check_status": "GET /cases/status/{case_id}",
            "get_results": "GET /cases/results/{case_id}"
        },
        "documentation": "/docs"
    }

# Create the FastAPI app and include the router
app = FastAPI()
app.include_router(api_router)