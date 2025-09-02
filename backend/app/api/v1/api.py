# Main API router for v1 endpoints

from fastapi import APIRouter

from app.api.v1 import auth, users, consultations, files

api_router = APIRouter()

# Include all API routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(consultations.router, prefix="/consultations", tags=["consultations"])
api_router.include_router(files.router, prefix="/files", tags=["files"])