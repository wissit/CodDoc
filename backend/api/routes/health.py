from fastapi import APIRouter
from datetime import datetime
from services.llm_service import llm_service

router = APIRouter(prefix="/api", tags=["Health"])


@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns the health status of the API and available LLM providers.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "llm_providers": llm_service.get_available_providers()
    }


@router.get("/config/llm-providers")
async def get_llm_providers():
    """
    Get available LLM providers.
    
    Returns list of configured and available LLM providers.
    """
    return {
        "providers": llm_service.get_available_providers()
    }
