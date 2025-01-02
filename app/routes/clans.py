import json
import pathlib
from fastapi import APIRouter, Depends
from app.models import SearchClans
from app.auth.auth_bearer import JWTBearer


router = APIRouter(tags=["clans"],
                   dependencies=[Depends(JWTBearer())],
                   arbitrary_types_allowed=True
                   )

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