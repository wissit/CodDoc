# API routes package
from .analysis import router as analysis_router
from .documentation import router as documentation_router
from .reviews import router as reviews_router
from .health import router as health_router

__all__ = [
    "analysis_router",
    "documentation_router",
    "reviews_router",
    "health_router"
]
