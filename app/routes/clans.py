import pathlib
import json
from fastapi import APIRouter, Request, Depends
from app.models.models import SearchClans
from app.auth.auth_bearer import JWTBearer
from app.routes.config import config_store

router = APIRouter(tags=["clans"])


@router.get('/clans/{clanTag}/currentwar/leaguegroup',
            summary="Retrieve information about clan's current clan war league group",
            description="Retrieve information about clan's current clan war league group")
async def get_clans_currentwar_leaguegroup(clanTag: str, request: Request):
    #let them set different config for each endpoint, so u could even have different depending on clan
    response_type = config_store.get(request.client.host, {}).get('/clans/{clanTag}/currentwar/leaguegroup', "NOTFOUND")
    path = pathlib.Path(f"data/clans/leaguegroup/{response_type}.json")
    with open(str(path)) as file:
        data = json.load(file)
    return data



@router.get('/clans',
            summary="Search clans",
            description="This endpoint is cached for each clan tag. The maximum lifetime of the cache is 2 minutes.")
async def search_clans(test: str) -> SearchClans:
    "Test description"
    path = pathlib.Path("data/clans/search/CLANS_FOUND.json")
    with open(str(path)) as data:
        data = data.read()
        return SearchClans.model_validate_json(json_data=data)

@router.get('/clans/{clan_tag}',
            summary='Get clan information',
            description="Get information about a clan with the given clan tag. This endpoint is cached for each clan "
                        "tag. The maximum lifetime of the cache is 2 minutes.")
async def get_clan(clan_tag: str):
    "Test Test"
    return 'test'