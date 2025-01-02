from fastapi import APIRouter

from app.routes.clans import router as clans_router

router = APIRouter()

router.include_router(clans_router, tags=["clans"])