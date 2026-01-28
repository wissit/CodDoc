from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel, Field
from database import get_db
from models import Documentation
from services.llm_service import llm_service

router = APIRouter(prefix="/api", tags=["Documentation"])


class DocumentRequest(BaseModel):
    """Request model for documentation generation."""
    code: str = Field(..., description="The code to document")
    language: str = Field(..., description="Programming language")
    filename: Optional[str] = Field(None, description="Optional filename")
    doc_style: Optional[str] = Field("google", description="Documentation style")
    llm_provider: Optional[str] = Field("gemini", description="LLM provider to use")


class DocumentResponse(BaseModel):
    """Response model for documentation generation."""
    doc_id: str
    code: str
    language: str
    documentation: dict
    created_at: str


@router.post("/document", response_model=DocumentResponse)
async def generate_documentation(request: DocumentRequest, db: Session = Depends(get_db)):
    """
    Generate comprehensive documentation for code.
    
    This endpoint generates documentation including:
    - Function/class descriptions
    - Parameter documentation
    - Return value documentation
    - Usage examples
    """
    try:
        # Get LLM provider
        provider = llm_service.get_provider(request.llm_provider)
        
        # Generate documentation
        documentation = provider.generate_documentation(
            code=request.code,
            language=request.language,
            doc_style=request.doc_style or "google"
        )
        
        # Save to database
        doc = Documentation(
            code=request.code,
            language=request.language,
            filename=request.filename,
            documentation=documentation,
            doc_style=request.doc_style or "google",
            llm_provider=request.llm_provider or "gemini"
        )
        
        db.add(doc)
        db.commit()
        db.refresh(doc)
        
        return DocumentResponse(
            doc_id=doc.id,
            code=doc.code,
            language=doc.language,
            documentation=doc.documentation,
            created_at=doc.created_at.isoformat()
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating documentation: {str(e)}")
