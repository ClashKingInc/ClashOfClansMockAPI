from fastapi import APIRouter, Query

from app.models import (
    ClanBuilderBaseRankingListResponse,
    ClanCapitalRankingListResponse,
    ClanRankingListResponse,
    Location,
    LocationListResponse,
    PlayerBuilderBaseRankingListResponse,
    PlayerRankingListResponse,
)
from app.routes.common import STANDARD_ERROR_RESPONSES, respond_from_fixture, respond_item_from_list_fixture, respond_location_rankings_fixture, validate_paging


router = APIRouter()


@router.get("/locations/{locationId}/rankings/clans", tags=["locations"], response_model=ClanRankingListResponse, responses=STANDARD_ERROR_RESPONSES)
async def get_clan_ranking(locationId: str, limit: int | None = Query(default=None, ge=1), after: str | None = None, before: str | None = None):
    paging_error = validate_paging(after, before)
    if paging_error:
        return paging_error
    return respond_location_rankings_fixture("rankings/clans", locationId, limit=limit, after=after, before=before, rewrite_embedded_location=True)


@router.get("/locations/{locationId}/rankings/players", tags=["locations"], response_model=PlayerRankingListResponse, responses=STANDARD_ERROR_RESPONSES)
async def get_player_ranking(locationId: str, limit: int | None = Query(default=None, ge=1), after: str | None = None, before: str | None = None):
    paging_error = validate_paging(after, before)
    if paging_error:
        return paging_error
    return respond_location_rankings_fixture("rankings/players", locationId, limit=limit, after=after, before=before)


@router.get("/locations/{locationId}/rankings/players-builder-base", tags=["locations"], response_model=PlayerBuilderBaseRankingListResponse, responses=STANDARD_ERROR_RESPONSES)
async def get_player_builder_base_ranking(locationId: str, limit: int | None = Query(default=None, ge=1), after: str | None = None, before: str | None = None):
    paging_error = validate_paging(after, before)
    if paging_error:
        return paging_error
    return respond_location_rankings_fixture("rankings/players-builder-base", locationId, limit=limit, after=after, before=before)


@router.get("/locations/{locationId}/rankings/clans-builder-base", tags=["locations"], response_model=ClanBuilderBaseRankingListResponse, responses=STANDARD_ERROR_RESPONSES)
async def get_clan_builder_base_ranking(locationId: str, limit: int | None = Query(default=None, ge=1), after: str | None = None, before: str | None = None):
    paging_error = validate_paging(after, before)
    if paging_error:
        return paging_error
    return respond_location_rankings_fixture("rankings/clans-builder-base", locationId, limit=limit, after=after, before=before, rewrite_embedded_location=True)


@router.get("/locations", tags=["locations"], response_model=LocationListResponse, responses=STANDARD_ERROR_RESPONSES)
async def get_locations(limit: int | None = Query(default=None, ge=1), after: str | None = None, before: str | None = None):
    paging_error = validate_paging(after, before)
    if paging_error:
        return paging_error
    return respond_from_fixture("locations/LISTLOCATIONS.json", limit=limit, after=after, before=before)


@router.get("/locations/{locationId}/rankings/capitals", tags=["locations"], response_model=ClanCapitalRankingListResponse, responses=STANDARD_ERROR_RESPONSES)
async def get_clan_capital_ranking(locationId: str, limit: int | None = Query(default=None, ge=1), after: str | None = None, before: str | None = None):
    paging_error = validate_paging(after, before)
    if paging_error:
        return paging_error
    return respond_location_rankings_fixture("rankings/capitals", locationId, limit=limit, after=after, before=before, rewrite_embedded_location=True)


@router.get("/locations/{locationId}", tags=["locations"], response_model=Location, responses=STANDARD_ERROR_RESPONSES)
async def get_location(locationId: str):
    return respond_item_from_list_fixture("locations/LISTLOCATIONS.json", locationId, "locations/location/BADREQUEST.json")
