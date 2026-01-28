from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel
from database import get_db
from models import CodeReview

router = APIRouter(prefix="/api", tags=["Reviews"])


class ReviewSummary(BaseModel):
    """Summary model for review list."""
    review_id: str
    language: str
    quality_score: Optional[float]
    created_at: str
    filename: Optional[str]


class PaginationInfo(BaseModel):
    """Pagination information."""
    page: int
    limit: int
    total: int
    pages: int


class ReviewsListResponse(BaseModel):
    """Response model for review list."""
    reviews: List[ReviewSummary]
    pagination: PaginationInfo


class ReviewDetailResponse(BaseModel):
    """Response model for review detail."""
    review_id: str
    code: str
    language: str
    filename: Optional[str]
    analysis: dict
    created_at: str


@router.get("/reviews", response_model=ReviewsListResponse)
async def get_reviews(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    language: Optional[str] = Query(None, description="Filter by language"),
    db: Session = Depends(get_db)
):
    """
    Get paginated list of code reviews.
    
    Supports filtering by programming language and pagination.
    """
    try:
        # Build query
        query = db.query(CodeReview)
        
        if language:
            query = query.filter(CodeReview.language == language)
        
        # Get total count
        total = query.count()
        
        # Calculate pagination
        pages = (total + limit - 1) // limit
        offset = (page - 1) * limit
        
        # Get reviews
        reviews = query.order_by(CodeReview.created_at.desc()).offset(offset).limit(limit).all()
        
        # Convert to response
        review_summaries = [
            ReviewSummary(
                review_id=r.id,
                language=r.language,
                quality_score=r.quality_score,
                created_at=r.created_at.isoformat(),
                filename=r.filename
            )
            for r in reviews
        ]
        
        return ReviewsListResponse(
            reviews=review_summaries,
            pagination=PaginationInfo(
                page=page,
                limit=limit,
                total=total,
                pages=pages
            )
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching reviews: {str(e)}")


@router.get("/reviews/{review_id}", response_model=ReviewDetailResponse)
async def get_review(review_id: str, db: Session = Depends(get_db)):
    """
    Get specific code review by ID.
    """
    try:
        review = db.query(CodeReview).filter(CodeReview.id == review_id).first()
        
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        
        return ReviewDetailResponse(
            review_id=review.id,
            code=review.code,
            language=review.language,
            filename=review.filename,
            analysis=review.analysis,
            created_at=review.created_at.isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching review: {str(e)}")


@router.delete("/reviews/{review_id}", status_code=204)
async def delete_review(review_id: str, db: Session = Depends(get_db)):
    """
    Delete a specific code review.
    """
    try:
        review = db.query(CodeReview).filter(CodeReview.id == review_id).first()
        
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        
        db.delete(review)
        db.commit()
        
        return None
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting review: {str(e)}")
