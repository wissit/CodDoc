from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from config import settings
from database import init_db
from api.routes import (
    analysis_router,
    documentation_router,
    reviews_router,
    health_router
)

# Create FastAPI app
app = FastAPI(
    title="CodDoc AI API",
    description="AI-Powered Code Review & Documentation Assistant",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS
origins = settings.cors_origins.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router)
app.include_router(analysis_router)
app.include_router(documentation_router)
app.include_router(reviews_router)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    init_db()
    print("✅ Database initialized")
    print(f"✅ CodDoc AI API started on {settings.api_host}:{settings.api_port}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    print("👋 CodDoc AI API shutting down")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to CodDoc AI API",
        "docs": "/docs",
        "health": "/api/health"
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.environment == "development" else "An error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload
    )
