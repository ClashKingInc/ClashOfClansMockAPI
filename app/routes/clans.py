from fastapi import APIRouter, Query

from app.models import (
    CapitalRaidSeasonsResponse,
    Clan,
    ClanMembersResponse,
    ClanSearchResponse,
    ClanWar,
    ClanWarLeagueGroup,
    ClanWarLogResponse,
)
from app.routes.common import (
    STANDARD_ERROR_RESPONSES,
    pick_variant,
    respond_from_fixture,
    unsupported_variant_response,
    validate_paging,
    validate_tag,
    variant_offset,
)


router = APIRouter()


@router.get("/clans/{clanTag}/currentwar/leaguegroup", tags=["clans"], response_model=ClanWarLeagueGroup, responses=STANDARD_ERROR_RESPONSES)
async def get_clan_war_league_group(clanTag: str):
    normalized_tag, error = validate_tag(clanTag)
    if error:
        return error
    fixture_name = pick_variant(normalized_tag, ["INWAR", "ENDED", "NOTFOUND"])
    if fixture_name is None:
        return unsupported_variant_response(normalized_tag)
    return respond_from_fixture(f"clans/leaguegroup/{fixture_name}.json")


@router.get("/clanwarleagues/wars/{warTag}", tags=["clans"], response_model=ClanWar, responses=STANDARD_ERROR_RESPONSES)
async def get_clan_war_league_war(warTag: str):
    normalized_tag, error = validate_tag(warTag)
    if error:
        return error
    fixture_name = pick_variant(normalized_tag, ["INWAR", "PREPARATION", "ENDED"])
    if fixture_name is None:
        return unsupported_variant_response(normalized_tag)
    return respond_from_fixture(f"clans/clanwarleagues/{fixture_name}.json")


@router.get("/clans/{clanTag}/warlog", tags=["clans"], response_model=ClanWarLogResponse, responses=STANDARD_ERROR_RESPONSES)
async def get_clan_war_log(clanTag: str, limit: int | None = Query(default=None, ge=1), after: str | None = None, before: str | None = None):
    paging_error = validate_paging(after, before)
    if paging_error:
        return paging_error
    normalized_tag, error = validate_tag(clanTag)
    if error:
        return error
    fixture_name = pick_variant(normalized_tag, ["WARLOG", "ACCESSDENIED"])
    if fixture_name is None:
        return unsupported_variant_response(normalized_tag)
    return respond_from_fixture(f"clans/warlog/{fixture_name}.json", limit=limit, after=after, before=before)


@router.get("/clans", tags=["clans"], response_model=ClanSearchResponse, responses=STANDARD_ERROR_RESPONSES)
async def search_clans(
    name: str | None = None,
    warFrequency: str | None = None,
    locationId: int | None = None,
    minMembers: int | None = None,
    maxMembers: int | None = None,
    minClanPoints: int | None = None,
    minClanLevel: int | None = None,
    limit: int | None = Query(default=None, ge=1),
    after: str | None = None,
    before: str | None = None,
    labelIds: str | None = None,
):
    paging_error = validate_paging(after, before)
    if paging_error:
        return paging_error
    return respond_from_fixture("clans/search/CLANS_FOUND.json", limit=limit, after=after, before=before)


@router.get("/clans/{clanTag}/currentwar", tags=["clans"], response_model=ClanWar, responses=STANDARD_ERROR_RESPONSES)
async def get_current_war(clanTag: str):
    normalized_tag, error = validate_tag(clanTag)
    if error:
        return error
    fixture_name = pick_variant(normalized_tag, ["INWAR", "PREPARATION", "ENDED", "NOTINWAR", "ACCESSDENIED"])
    if fixture_name is None:
        return unsupported_variant_response(normalized_tag)
    return respond_from_fixture(f"clans/currentwar/{fixture_name}.json")


@router.get("/clans/{clanTag}", tags=["clans"], response_model=Clan, responses=STANDARD_ERROR_RESPONSES)
async def get_clan(clanTag: str):
    normalized_tag, error = validate_tag(clanTag)
    if error:
        return error
    if variant_offset(normalized_tag) > 0:
        return unsupported_variant_response(normalized_tag)
    return respond_from_fixture("clans/clans/CLAN.json")


@router.get("/clans/{clanTag}/members", tags=["clans"], response_model=ClanMembersResponse, responses=STANDARD_ERROR_RESPONSES)
async def get_clan_members(clanTag: str, limit: int | None = Query(default=None, ge=1), after: str | None = None, before: str | None = None):
    paging_error = validate_paging(after, before)
    if paging_error:
        return paging_error
    normalized_tag, error = validate_tag(clanTag)
    if error:
        return error
    if variant_offset(normalized_tag) > 0:
        return unsupported_variant_response(normalized_tag)
    return respond_from_fixture("clans/members/MEMBERS.json", limit=limit, after=after, before=before)


@router.get("/clans/{clanTag}/capitalraidseasons", tags=["clans"], response_model=CapitalRaidSeasonsResponse, responses=STANDARD_ERROR_RESPONSES)
async def get_capital_raid_seasons(clanTag: str, limit: int | None = Query(default=None, ge=1), after: str | None = None, before: str | None = None):
    paging_error = validate_paging(after, before)
    if paging_error:
        return paging_error
    normalized_tag, error = validate_tag(clanTag)
    if error:
        return error
    if variant_offset(normalized_tag) > 0:
        return unsupported_variant_response(normalized_tag)
    return respond_from_fixture("clans/capitalraidseasons/CAPITALRAIDSEASON.json", limit=limit, after=after, before=before)
