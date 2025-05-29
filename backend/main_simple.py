# Replace the probate endpoint in main_simple.py
@app.post("/api/v1/cases/probate")
async def create_probate_case(case_data: Dict[str, Any], background_tasks: BackgroundTasks):
    """Create a new probate case with full CrewAI processing"""
    try:
        case_id = f"PROB_{uuid.uuid4().hex[:8].upper()}"
        case_data["case_id"] = case_id
        
        # Store initial case info
        case_results[case_id] = {
            "status": "processing",
            "created_at": datetime.now().isoformat(),
            "case_type": "probate",
            "case_data": case_data
        }
        
        # Process with CrewAI in background
        background_tasks.add_task(process_probate_with_crewai, case_id, case_data)
        
        return {
            "success": True,
            "case_id": case_id,
            "status": "processing",
            "message": "🤖 CrewAI agents are analyzing your probate case",
            "estimated_time": "3-5 minutes",
            "agents_working": [
                "Document Analyst",
                "Legal Advisor",
                "Tax Specialist", 
                "Compliance Officer",
                "Case Manager"
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating case: {str(e)}")

# Add background processing function
async def process_probate_with_crewai(case_id: str, case_data: Dict[str, Any]):
    """Background task to process probate case with CrewAI"""
    try:
        print(f"🚀 Starting CrewAI processing for case {case_id}")
        
        # Import and create CrewAI crew
        from app.crews.probate_crew import ProbateCrew
        crew = ProbateCrew()
        
        # Process the case with full CrewAI
        results = crew.process_probate_case(case_data)
        
        # Update stored results
        case_results[case_id]["status"] = "completed"
        case_results[case_id]["results"] = results
        case_results[case_id]["completed_at"] = datetime.now().isoformat()
        
        print(f"✅ CrewAI processing completed for case {case_id}")
        
    except Exception as e:
        print(f"❌ CrewAI processing failed for case {case_id}: {e}")
        case_results[case_id]["status"] = "error"
        case_results[case_id]["error"] = str(e)