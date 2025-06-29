from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
import asyncio
from crewai import Crew, Process,Agent,Task
from agents import doctor
from task import help_patients
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent

from agents import doctor, verifier, nutritionist, exercise_specialist
from task import help_patients, verification, nutrition_analysis, exercise_planning
app = FastAPI(title="Blood Test Report Analyser")

def run_crew(query: str, file_path: str):
    """Run the medical analysis crew with proper error handling"""
    try:
        medical_crew = Crew(
            agents=[verifier, doctor, nutritionist],
            tasks=[verification, help_patients, nutrition_analysis],
            process=Process.sequential,
            verbose=True  # Enable verbose for debugging
        )

        # Pass both query and file_path as inputs
        result = medical_crew.kickoff(inputs={
            "query": query, 
            "file_path": file_path
        })
        
        return result
        
    except Exception as e:
        print(f"Crew execution error: {str(e)}")
        raise e

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Blood Test Report Analyser API is running"}

@app.post("/analyze")
async def analyze_blood_report(
    file: UploadFile = File(...),
    query: str = Form(default="Summarise my Blood Test Report")
):
    """Analyze blood test report and provide comprehensive health recommendations"""
    
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    # Generate unique filename to avoid conflicts
    file_id = str(uuid.uuid4())
    file_path = f"data/blood_test_report_{file_id}.pdf"
    
    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Validate file was saved
        if not os.path.exists(file_path):
            raise HTTPException(status_code=500, detail="Failed to save uploaded file")
            
        # Validate query
        if not query or query.strip() == "":
            query = "Summarise my Blood Test Report"
            
        print(f"Processing file: {file_path}")
        print(f"Query: {query}")
        
        # Process the blood report with all specialists
        response = run_crew(query=query.strip(), file_path=file_path)
        
        return {
            "status": "success",
            "query": query,
            "analysis": str(response),
            "file_processed": file.filename
        }
        
    except Exception as e:
        print(f"Error in analyze_blood_report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing blood report: {str(e)}")
    
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Cleaned up file: {file_path}")
            except Exception as cleanup_error:
                print(f"Cleanup error: {cleanup_error}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)