from typing import Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse

from app.auth.auth_bearer import JWTBearer
from app.models import ClientError

openapi_tags = [{"name"       : "clans",
                 "description": "Access clan specific information"},
                {"name"       : "players",
                 "description": "Access player specific information"},
                {"name"       : "leagues",
                 "description": "Access league information"},
                {"name"       : "locations",
                 "description": "Access global and local rankings"},
                {"name"       : "goldpass",
                 "description": "Access information about gold pass"},
                {"name"       : "labels",
                 "description": "Access information about clan and player labels"}
                ]

app = FastAPI(openapi_tags=openapi_tags, dependencies=[Depends(JWTBearer())])

from app.routes import router as api_router

app.include_router(api_router)


@app.exception_handler(ClientError)
async def unicorn_exception_handler(request: Request, exc: ClientError):
	return JSONResponse(
			status_code=exc.status,
			content={"message": exc.message, "reason": exc.reason},
	)

