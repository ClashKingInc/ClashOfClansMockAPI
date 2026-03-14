from fastapi import APIRouter, Query

from app.models import (
    BuilderBaseLeague,
    BuilderBaseLeagueListResponse,
    CapitalLeague,
    CapitalLeagueListResponse,
    LeagueGroup,
    LeagueSeasonListResponse,
    LeagueTier,
    LeagueTierListResponse,
    PlayerRankingListResponse,
    WarLeague,
    WarLeagueListResponse,
)
from app.routes.common import (
    STANDARD_ERROR_RESPONSES,
    error_response,
    missing_mock_response,
    normalize_tag,
    player_found_payload,
    read_wrapped_fixture,
    respond_from_fixture,
    respond_from_optional_fixture,
    respond_item_from_list_fixture,
    unsupported_variant_response,
    validate_paging,
    validate_tag,
    variant_offset,
)


router = APIRouter()


@router.get("/leaguetiers/{leagueTierId}", tags=["leagues"], response_model=LeagueTier, responses=STANDARD_ERROR_RESPONSES)
async def get_league_tier(leagueTierId: str):
    return respond_item_from_list_fixture("leagues/LISTLEAGUETIERS.json", leagueTierId, "leagues/leaguetier/BADREQUEST.json")


@router.get("/capitalleagues", tags=["leagues"], response_model=CapitalLeagueListResponse, responses=STANDARD_ERROR_RESPONSES)
async def get_capital_leagues(limit: int | None = Query(default=None, ge=1), after: str | None = None, before: str | None = None):
    paging_error = validate_paging(after, before)
    if paging_error:
        return paging_error
    return respond_from_optional_fixture("leagues/LISTCAPITALLEAGUES.json", limit=limit, after=after, before=before)


@router.get("/leaguetiers", tags=["leagues"], response_model=LeagueTierListResponse, responses=STANDARD_ERROR_RESPONSES)
async def get_league_tiers(limit: int | None = Query(default=None, ge=1), after: str | None = None, before: str | None = None):
    paging_error = validate_paging(after, before)
    if paging_error:
        return paging_error
    return respond_from_fixture("leagues/LISTLEAGUETIERS.json", limit=limit, after=after, before=before)


@router.get("/leagues", tags=["leagues"])
async def get_leagues(limit: int | None = Query(default=None, ge=1), after: str | None = None, before: str | None = None):
    paging_error = validate_paging(after, before)
    if paging_error:
        return paging_error
    return missing_mock_response()


@router.get("/leagues/{leagueId}/seasons/{seasonId}", tags=["leagues"], response_model=PlayerRankingListResponse, responses=STANDARD_ERROR_RESPONSES)
async def get_league_season_rankings(
    leagueId: str,
    seasonId: str,
    limit: int | None = Query(default=None, ge=1),
    after: str | None = None,
    before: str | None = None,
):
    paging_error = validate_paging(after, before)
    if paging_error:
        return paging_error
    if leagueId != "29000022":
        return respond_from_fixture("leagues/league-season/BADREQUEST.json")

    season_ids = {item["id"] for item in read_wrapped_fixture("leagues/LISTLEAGUESEASONS.json")["body"]["items"]}
    if seasonId not in season_ids:
        return error_response(404, "notFound", f"Season '{seasonId}' was not found.")
    return respond_from_fixture("leagues/league-season/LEAGUESEASON.json", limit=limit, after=after, before=before)


@router.get("/capitalleagues/{leagueId}", tags=["leagues"], response_model=CapitalLeague, responses=STANDARD_ERROR_RESPONSES)
async def get_capital_league(leagueId: str):
    return respond_item_from_list_fixture("leagues/LISTCAPITALLEAGUES.json", leagueId, "leagues/capital-league/BADREQUEST.json")


@router.get("/builderbaseleagues/{leagueId}", tags=["leagues"], response_model=BuilderBaseLeague, responses=STANDARD_ERROR_RESPONSES)
async def get_builder_base_league(leagueId: str):
    return respond_item_from_list_fixture("leagues/LISTBUILDERLEAGUES.json", leagueId, "leagues/builderbaseleague/BADREQUEST.json")


@router.get("/builderbaseleagues", tags=["leagues"], response_model=BuilderBaseLeagueListResponse, responses=STANDARD_ERROR_RESPONSES)
async def get_builder_base_leagues(limit: int | None = Query(default=None, ge=1), after: str | None = None, before: str | None = None):
    paging_error = validate_paging(after, before)
    if paging_error:
        return paging_error
    return respond_from_fixture("leagues/LISTBUILDERLEAGUES.json", limit=limit, after=after, before=before)


@router.get("/leagues/{leagueId}", tags=["leagues"])
async def get_league(leagueId: str):
    return missing_mock_response()


@router.get("/leaguegroup/{leagueGroupTag}/{leagueSeasonId}", tags=["leagues"], response_model=LeagueGroup, responses=STANDARD_ERROR_RESPONSES)
async def get_league_group(leagueGroupTag: str, leagueSeasonId: str, playerTag: str):
    normalized_player_tag, error = validate_tag(playerTag)
    if error:
        return error
    if variant_offset(normalized_player_tag) > 0:
        return unsupported_variant_response(normalized_player_tag)

    player = player_found_payload()
    current_group_tag = normalize_tag(str(player.get("currentLeagueGroupTag", "")))
    current_season_id = str(player.get("currentLeagueSeasonId"))
    previous_group_tag = normalize_tag(str(player.get("previousLeagueGroupTag", "")))
    previous_season_id = str(player.get("previousLeagueSeasonId"))
    requested_group_tag = normalize_tag(leagueGroupTag)

    if requested_group_tag == current_group_tag and leagueSeasonId == current_season_id:
        return respond_from_fixture("leagues/leaguegroup/CURRENT.json")
    if requested_group_tag == previous_group_tag and leagueSeasonId == previous_season_id:
        return respond_from_fixture("leagues/leaguegroup/PREVIOUS.json")
    return error_response(404, "notFound", "League group was not found.")


@router.get("/leagues/{leagueId}/seasons", tags=["leagues"], response_model=LeagueSeasonListResponse, responses=STANDARD_ERROR_RESPONSES)
async def get_league_seasons(leagueId: str, limit: int | None = Query(default=None, ge=1), after: str | None = None, before: str | None = None):
    paging_error = validate_paging(after, before)
    if paging_error:
        return paging_error
    if leagueId != "29000022":
        return respond_from_fixture("leagues/league-season/BADREQUEST.json")
    return respond_from_fixture("leagues/LISTLEAGUESEASONS.json", limit=limit, after=after, before=before)


@router.get("/warleagues/{leagueId}", tags=["leagues"], response_model=WarLeague, responses=STANDARD_ERROR_RESPONSES)
async def get_war_league(leagueId: str):
    return respond_item_from_list_fixture("leagues/LISTWARELEAGUES.json", leagueId, "leagues/war-league/BADREQUEST.json")


@router.get("/warleagues", tags=["leagues"], response_model=WarLeagueListResponse, responses=STANDARD_ERROR_RESPONSES)
async def get_war_leagues(limit: int | None = Query(default=None, ge=1), after: str | None = None, before: str | None = None):
    paging_error = validate_paging(after, before)
    if paging_error:
        return paging_error
    return respond_from_optional_fixture("leagues/LISTWARELEAGUES.json", limit=limit, after=after, before=before)
