from fastapi import APIRouter

from app.routes.clans import rounter as clans_router

router = APIRouter()

router.include_router(clans_rounter, tags=["Clans"])