from fastapi import APIRouter, Query

from app.models import LabelListResponse
from app.routes.common import STANDARD_ERROR_RESPONSES, respond_from_fixture, validate_paging


router = APIRouter()


@router.get("/labels/players", tags=["labels"], response_model=LabelListResponse, responses=STANDARD_ERROR_RESPONSES)
async def get_player_labels(limit: int | None = Query(default=None, ge=1), after: str | None = None, before: str | None = None):
    paging_error = validate_paging(after, before)
    if paging_error:
        return paging_error
    return respond_from_fixture("labels/players/PLAYERLABELS.json", limit=limit, after=after, before=before)


@router.get("/labels/clans", tags=["labels"], response_model=LabelListResponse, responses=STANDARD_ERROR_RESPONSES)
async def get_clan_labels(limit: int | None = Query(default=None, ge=1), after: str | None = None, before: str | None = None):
    paging_error = validate_paging(after, before)
    if paging_error:
        return paging_error
    return respond_from_fixture("labels/clans/CLANLABELS.json", limit=limit, after=after, before=before)
