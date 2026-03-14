from fastapi import APIRouter

from app.models import GoldPassSeason
from app.routes.common import STANDARD_ERROR_RESPONSES, respond_from_fixture


router = APIRouter()


@router.get("/goldpass/seasons/current", tags=["goldpass"], response_model=GoldPassSeason, responses=STANDARD_ERROR_RESPONSES)
async def get_current_gold_pass_season():
    return respond_from_fixture("goldpass/GOLDPASS.json")
