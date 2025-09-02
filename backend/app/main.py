# FastAPI main application entry point

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine
from app.models import models
from app.api.v1.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Create database tables on startup
    models.Base.metadata.create_all(bind=engine)
    
    # Create upload directory if it doesn't exist
    os.makedirs(settings.UPLOAD_DIRECTORY, exist_ok=True)
    
    yield
    # Cleanup on shutdown
    pass


# Create FastAPI application instance
app = FastAPI(
    title="AI Doctor Assistant",
    description="A medical analysis and emergency treatment recommendation system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

# Mount static files for uploaded content
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIRECTORY), name="uploads")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Doctor Assistant API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health"
    }


@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "AI Doctor Assistant"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )