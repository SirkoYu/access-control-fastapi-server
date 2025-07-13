from fastapi import APIRouter

from core.config import settings
from .user import router as users_router

api_router = APIRouter(prefix=settings.api.prefix)
api_router.include_router(users_router)