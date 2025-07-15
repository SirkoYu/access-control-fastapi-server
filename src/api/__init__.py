from fastapi import APIRouter

from src.core.config import settings
from .user import router as users_router
from .room import router as rooms_router
from .role import router as role_router
from .floor import router as floor_router
from .current_presence import router as current_presence_router
from .building import router as buildings_router
from .access_rule import router as access_rule_router
from .access_log import router as access_log_router

api_router = APIRouter(prefix=settings.api.prefix)

api_router.include_router(users_router)
api_router.include_router(rooms_router)
api_router.include_router(role_router)
api_router.include_router(floor_router)
api_router.include_router(current_presence_router)
api_router.include_router(buildings_router)
api_router.include_router(access_rule_router)
api_router.include_router(access_log_router)
