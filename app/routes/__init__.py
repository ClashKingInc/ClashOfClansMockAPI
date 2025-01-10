from fastapi import APIRouter

from app.routes.clans import router as clans_router
from app.routes.config import router as config_router
router = APIRouter()

router.include_router(clans_router)
router.include_router(config_router)