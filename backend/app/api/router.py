from fastapi import APIRouter

from app.api import auth, content, progress, admin

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(content.router, tags=["content"])
api_router.include_router(progress.router, tags=["progress"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])

