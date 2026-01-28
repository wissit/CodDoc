from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel, Field
from database import get_db
from models import CodeReview
from services.llm_service import llm_service

router = APIRouter(prefix="/api", tags=["Analysis"])


class AnalyzeRequest(BaseModel):
    """Request model for code analysis."""
    code: str = Field(..., description="The code to analyze")
    language: str = Field(..., description="Programming language")
    filename: Optional[str] = Field(None, description="Optional filename")
    llm_provider: Optional[str] = Field("gemini", description="LLM provider to use")


class AnalyzeResponse(BaseModel):
    """Response model for code analysis."""
    review_id: str
    code: str
    language: str
    analysis: dict
    created_at: str


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_code(request: AnalyzeRequest, db: Session = Depends(get_db)):
    """
    Analyze code and return AI-generated review.
    
    This endpoint analyzes the provided code and returns:
    - Code quality assessment
    - Security vulnerabilities
    - Performance suggestions
    - Best practice recommendations
    """
    try:
        # Get LLM provider
        provider = llm_service.get_provider(request.llm_provider)
        
        # Analyze code
        analysis = provider.analyze_code(
            code=request.code,
            language=request.language,
            filename=request.filename
        )
        
        # Extract quality score
        quality_score = analysis.get("quality_score", 0)
        
        # Save to database
        review = CodeReview(
            code=request.code,
            language=request.language,
            filename=request.filename,
            quality_score=quality_score,
            analysis=analysis,
            llm_provider=request.llm_provider or "gemini"
        )
        
        db.add(review)
        db.commit()
        db.refresh(review)
        
        return AnalyzeResponse(
            review_id=review.id,
            code=review.code,
            language=review.language,
            analysis=review.analysis,
            created_at=review.created_at.isoformat()
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing code: {str(e)}")
