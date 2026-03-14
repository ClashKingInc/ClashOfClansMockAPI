from fastapi import APIRouter, Body

from app.models import BattleLogResponse, LeagueHistoryResponse, Player, VerifyTokenRequest, VerifyTokenResponse
from app.routes.common import (
    STANDARD_ERROR_RESPONSES,
    pick_variant,
    respond_from_fixture,
    unsupported_variant_response,
    validate_tag,
    variant_offset,
)


router = APIRouter()


@router.get("/players/{playerTag}", tags=["players"], response_model=Player, responses=STANDARD_ERROR_RESPONSES)
async def get_player(playerTag: str):
    normalized_tag, error = validate_tag(playerTag)
    if error:
        return error
    fixture_name = pick_variant(normalized_tag, ["FOUND", "NOTFOUND"])
    if fixture_name is None:
        return unsupported_variant_response(normalized_tag)
    return respond_from_fixture(f"players/player/{fixture_name}.json")


@router.get("/players/{playerTag}/battlelog", tags=["players"], response_model=BattleLogResponse, responses=STANDARD_ERROR_RESPONSES)
async def get_battle_log(playerTag: str):
    normalized_tag, error = validate_tag(playerTag)
    if error:
        return error
    if variant_offset(normalized_tag) > 0:
        return unsupported_variant_response(normalized_tag)
    return respond_from_fixture("players/battlelog/LOG.json")


@router.post("/players/{playerTag}/verifytoken", tags=["players"], response_model=VerifyTokenResponse, responses=STANDARD_ERROR_RESPONSES)
async def verify_token(playerTag: str, body: VerifyTokenRequest = Body(...)):
    normalized_tag, error = validate_tag(playerTag)
    if error:
        return error
    fixture_name = pick_variant(normalized_tag, ["VALID", "NOTFOUND"])
    if fixture_name is None:
        return unsupported_variant_response(normalized_tag)
    if fixture_name == "NOTFOUND":
        return respond_from_fixture("players/verifytoken/NOTFOUND.json")
    if body.token == "TOKEN":
        return respond_from_fixture("players/verifytoken/VALID.json")
    return respond_from_fixture("players/verifytoken/INVALID.json")


@router.get("/players/{playerTag}/leaguehistory", tags=["players"], response_model=LeagueHistoryResponse, responses=STANDARD_ERROR_RESPONSES)
async def get_league_history(playerTag: str):
    normalized_tag, error = validate_tag(playerTag)
    if error:
        return error
    if variant_offset(normalized_tag) > 0:
        return unsupported_variant_response(normalized_tag)
    return respond_from_fixture("players/leaguehistory/LOG.json")
