
from fastapi import APIRouter, Request
from collections import defaultdict

router = APIRouter(tags=["config"])

config_store = defaultdict(lambda : defaultdict)


@router.post("/mock/configure")
def configure_mock(data: dict, request: Request):
    for endpoint, access_type in data.items():
        config_store[request.client.ip][endpoint] = access_type
    return {"message": f"Mock responses configured"}