from fastapi import APIRouter

from app.routes.clans import router as clans_router
from app.routes.goldpass import router as goldpass_router
from app.routes.labels import router as labels_router
from app.routes.leagues import router as leagues_router
from app.routes.locations import router as locations_router
from app.routes.players import router as players_router

router = APIRouter()

router.include_router(clans_router)
router.include_router(players_router)
router.include_router(leagues_router)
router.include_router(locations_router)
router.include_router(labels_router)
router.include_router(goldpass_router)
