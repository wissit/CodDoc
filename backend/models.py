from sqlalchemy import Column, String, Text, Float, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from database import Base


class CodeReview(Base):
    """Model for storing code review results."""
    
    __tablename__ = "code_reviews"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    code = Column(Text, nullable=False)
    language = Column(String(50), nullable=False)
    filename = Column(String(255), nullable=True)
    quality_score = Column(Float, nullable=True)
    analysis = Column(JSON, nullable=False)
    llm_provider = Column(String(50), default="gemini")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "review_id": self.id,
            "code": self.code,
            "language": self.language,
            "filename": self.filename,
            "quality_score": self.quality_score,
            "analysis": self.analysis,
            "llm_provider": self.llm_provider,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class Documentation(Base):
    """Model for storing generated documentation."""
    
    __tablename__ = "documentation"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    code = Column(Text, nullable=False)
    language = Column(String(50), nullable=False)
    filename = Column(String(255), nullable=True)
    documentation = Column(JSON, nullable=False)
    doc_style = Column(String(50), default="google")
    llm_provider = Column(String(50), default="gemini")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "doc_id": self.id,
            "code": self.code,
            "language": self.language,
            "filename": self.filename,
            "documentation": self.documentation,
            "doc_style": self.doc_style,
            "llm_provider": self.llm_provider,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
