from fastapi import APIRouter, Depends

from app.auth.auth_bearer import JWTBearer

router = APIRouter(tags=["clans"], dependencies=[Depends(JWTBearer())])