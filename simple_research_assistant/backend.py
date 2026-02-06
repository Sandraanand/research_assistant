"""
Simplified FastAPI Backend
Clean and minimal implementation
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uuid
from datetime import datetime

from config import config
from database import init_db, get_db, PaperSubmission
from orchestrator import get_orchestrator

# Initialize FastAPI
app = FastAPI(title="Simple Research Assistant", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup():
    config.validate()
    init_db()
    print("✅ Backend initialized")


# ==================== Request/Response Models ====================

class ResearchRequest(BaseModel):
    topic: str
    max_papers: int = 5


class ConceptRequest(BaseModel):
    concept: str
    context: Optional[str] = None


class PaperCheckRequest(BaseModel):
    title: str
    content: str


class PaperSubmitRequest(BaseModel):
    title: str
    authors: List[str]
    content: str
    professor_email: str


# ==================== API Endpoints ====================

@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "running",
        "message": "Simple Research Assistant API",
        "version": "1.0.0"
    }


@app.post("/api/research")
async def run_research(request: ResearchRequest):
    """
    Run complete research workflow
    - Literature search
    - Paper synthesis
    - Research extensions
    """
    try:
        orch = get_orchestrator()
        results = await orch.run_research_workflow(
            topic=request.topic,
            max_papers=request.max_papers
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/explain")
async def explain_concept(request: ConceptRequest):
    """Explain a concept in simple terms"""
    try:
        orch = get_orchestrator()
        explanation = await orch.explain_concept(
            concept=request.concept,
            context=request.context
        )
        return {"concept": request.concept, "explanation": explanation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/check-paper")
async def check_paper(request: PaperCheckRequest):
    """Check paper formatting"""
    try:
        orch = get_orchestrator()
        feedback = await orch.check_paper(
            title=request.title,
            content=request.content
        )
        return feedback
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/submit-paper")
async def submit_paper(request: PaperSubmitRequest):
    """Submit paper to database"""
    try:
        # Generate submission ID
        submission_id = f"SUB-{uuid.uuid4().hex[:8].upper()}"
        
        # Check formatting first
        orch = get_orchestrator()
        feedback = await orch.check_paper(
            title=request.title,
            content=request.content
        )
        
        # Store in database
        db = next(get_db())
        submission = PaperSubmission(
            submission_id=submission_id,
            title=request.title,
            authors=", ".join(request.authors),
            content=request.content,
            professor_email=request.professor_email,
            status="submitted",
            feedback=str(feedback)
        )
        db.add(submission)
        db.commit()
        
        return {
            "submission_id": submission_id,
            "status": "submitted",
            "message": f"Paper submitted to {request.professor_email}",
            "submitted_at": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/submission/{submission_id}")
async def get_submission_status(submission_id: str):
    """Check submission status"""
    try:
        db = next(get_db())
        submission = db.query(PaperSubmission).filter(
            PaperSubmission.submission_id == submission_id
        ).first()
        
        if not submission:
            raise HTTPException(status_code=404, detail="Submission not found")
        
        return {
            "submission_id": submission.submission_id,
            "title": submission.title,
            "status": submission.status,
            "submitted_at": submission.submitted_at.isoformat(),
            "feedback": submission.feedback
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=config.BACKEND_PORT)
