"""
API endpoints - These are the web addresses that handle requests
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any
import uuid
from datetime import datetime
import asyncio

# Import our AI crews
from app.crews.probate_crew import ProbateCrew
from app.crews.divorce_crew import DivorceCrew

# Create a router (like a section of our website)
router = APIRouter()

# Store case results in memory (in real app, this would be a database)
case_results = {}

@router.post("/probate")
async def create_probate_case(case_data: Dict[str, Any], background_tasks: BackgroundTasks):
    """
    Create a new probate case
    This is what happens when someone submits a probate form
    """
    try:
        # Create a unique case ID
        case_id = f"PROB_{uuid.uuid4().hex[:8].upper()}"
        case_data["case_id"] = case_id
        
        # Store initial case info
        case_results[case_id] = {
            "status": "processing",
            "created_at": datetime.now().isoformat(),
            "case_type": "probate",
            "case_data": case_data
        }
        
        # Start processing in the background
        background_tasks.add_task(process_probate_background, case_id, case_data)
        
        return {
            "success": True,
            "case_id": case_id,
            "status": "processing",
            "message": "🚀 Your probate case is being analyzed by our AI agents",
            "estimated_time": "2-5 minutes"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating case: {str(e)}")

@router.post("/divorce")
async def create_divorce_case(case_data: Dict[str, Any], background_tasks: BackgroundTasks):
    """
    Create a new divorce case
    This is what happens when someone submits a divorce form
    """
    try:
        # Create a unique case ID
        case_id = f"DIV_{uuid.uuid4().hex[:8].upper()}"
        case_data["case_id"] = case_id
        
        # Store initial case info
        case_results[case_id] = {
            "status": "processing",
            "created_at": datetime.now().isoformat(),
            "case_type": "divorce",
            "case_data": case_data
        }
        
        # Start processing in the background
        background_tasks.add_task(process_divorce_background, case_id, case_data)
        
        return {
            "success": True,
            "case_id": case_id,
            "status": "processing",
            "message": "🚀 Your divorce case is being analyzed by our AI agents",
            "estimated_time": "3-7 minutes"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating case: {str(e)}")

@router.get("/status/{case_id}")
async def get_case_status(case_id: str):
    """
    Check the status of a case
    """
    if case_id not in case_results:
        raise HTTPException(status_code=404, detail="Case not found")
    
    case = case_results[case_id]
    
    return {
        "case_id": case_id,
        "status": case["status"],
        "case_type": case["case_type"],
        "created_at": case["created_at"],
        "progress": "🤖 AI agents are working..." if case["status"] == "processing" else "✅ Complete"
    }

@router.get("/results/{case_id}")
async def get_case_results(case_id: str):
    """
    Get the results of a completed case
    """
    if case_id not in case_results:
        raise HTTPException(status_code=404, detail="Case not found")
    
    case = case_results[case_id]
    
    if case["status"] != "completed":
        raise HTTPException(status_code=400, detail="Case is still processing")
    
    return {
        "case_id": case_id,
        "results": case.get("results", {}),
        "status": "completed"
    }

# Background processing functions
async def process_probate_background(case_id: str, case_data: Dict[str, Any]):
    """
    Process probate case in the background
    """
    try:
        print(f"🚀 Starting probate case processing for {case_id}")
        
        # Create our AI crew
        crew = ProbateCrew()
        
        # Process the case (this might take a few minutes)
        results = crew.process_probate_case(case_data)
        
        # Update the stored results
        case_results[case_id]["status"] = "completed"
        case_results[case_id]["results"] = results
        case_results[case_id]["completed_at"] = datetime.now().isoformat()
        
        print(f"✅ Probate case {case_id} completed successfully")
        
    except Exception as e:
        print(f"❌ Error processing probate case {case_id}: {e}")
        case_results[case_id]["status"] = "error"
        case_results[case_id]["error"] = str(e)

async def process_divorce_background(case_id: str, case_data: Dict[str, Any]):
    """
    Process divorce case in the background
    """
    try:
        print(f"🚀 Starting divorce case processing for {case_id}")
        
        # Create our AI crew
        crew = DivorceCrew()
        
        # Process the case
        results = crew.process_divorce_case(case_data)
        
        # Update the stored results
        case_results[case_id]["status"] = "completed"
        case_results[case_id]["results"] = results
        case_results[case_id]["completed_at"] = datetime.now().isoformat()
        
        print(f"✅ Divorce case {case_id} completed successfully")
        
    except Exception as e:
        print(f"❌ Error processing divorce case {case_id}: {e}")
        case_results[case_id]["status"] = "error"
        case_results[case_id]["error"] = str(e)