import asyncio
from typing import Annotated
import uvicorn
from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from app.models import *
from app.auth.auth_bearer import JWTBearer


openapi_tags = [{"name": "clans",
                 "description": "Access clan specific information"},
                {"name": "players",
                 "description": "Access player specific information"},
                {"name": "leagues",
                 "description": "Access league information"},
                {"name": "locations",
                 "description": "Access global and local rankings"},
                {"name": "goldpass",
                 "description": "Access information about gold pass"},
                {"name": "labels",
                 "description": "Access information about clan and player labels"}
                ]

app = FastAPI(openapi_tags=openapi_tags,
              arbitrary_types_allowed=True,
              #dependencies=[Depends(JWTBearer())],
              title="Clash of Clans example API",
              summary="A Community project maintained by the Clash of Clans API Developer community to provide access "
                      "to all possible api responses at every time.",
              description="This project is not affiliated with with Supercell or Clash of Clans. It is a community "
                          "maintained tool to provide new developers an easy way to test their code. Responsible for "
                          "this is project are the administrators of the Clash of Clans API Developer discord server.\n"
                          "This API should mimic the original Clash of Clans API, but improve the developer experience "
                          "by extending the given API documentation with helpful information and better model hierarchy"
                          ". Additionally example responses were collected and are available under specify input "
                          "parameters. These example responses can be found at `https://github.com/doluk/coc_test_api`."
                          " Similar to the official API this API requires authentication with a bearer token. You can "
                          "either use an API key of the official API or, if you don't feel comfortable with using the "
                          "key of the official API, you can use `DEMO_TOKEN`.\n\nAll endpoints are cached, you can "
                          "get the remaining lifetime of the cache from the `cache-control` header, which can either "
                          "has the format `max-age=` or `public max-age=` of the response.")

from app.routes import router as api_router

app.include_router(api_router)


@app.exception_handler(ClientError)
async def unicorn_exception_handler(request: Request, exc: ClientError):
    return JSONResponse(
        status_code=exc.status,
        content={"message": exc.message, "reason": exc.reason},
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000)
