import json
import os
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse, JSONResponse

from app.models import *


openapi_tags = [
    {"name": "clans", "description": "Access clan specific information"},
    {"name": "players", "description": "Access player specific information"},
    {"name": "leagues", "description": "Access league information"},
    {"name": "locations", "description": "Access global and local rankings"},
    {"name": "goldpass", "description": "Access information about gold pass"},
    {"name": "labels", "description": "Access information about clan and player labels"},
]

ROOT = Path(__file__).resolve().parent
CUSTOM_DOCS_PATH = ROOT / "openapi.extensions.json"
EXCLUDED_PATHS = {"/leagues", "/leagues/{leagueId}"}
MOCK_PROXY_URL = os.getenv("MOCK_PROXY_URL", "http://localhost:8000")

app = FastAPI(
    openapi_tags=openapi_tags,
    arbitrary_types_allowed=True,
    docs_url=None,
    redoc_url=None,
    title="Clash of Clans example API",
    summary=(
        "A Community project maintained by the Clash of Clans API Developer community "
        "to provide access to all possible api responses at every time."
    ),
    description=(
        "This project is not affiliated with with Supercell or Clash of Clans. It is a community "
        "maintained tool to provide new developers an easy way to test their code. Responsible for "
        "this is project are the administrators of the Clash of Clans API Developer discord server.\n"
        "This API should mimic the original Clash of Clans API, but improve the developer experience "
        "by extending the given API documentation with helpful information and better model hierarchy"
        ". Code for this project can be found at https://github.com/ClashKingInc/ClashOfClansMockAPI. All"
        " endpoints that take tags respond to #2PP with variants being produced via appending Ps."
    ),
)


def _load_custom_extensions() -> dict:
    if not CUSTOM_DOCS_PATH.exists():
        return {}
    return json.loads(CUSTOM_DOCS_PATH.read_text())


def _merge_operation_extensions(schema: dict, extensions: dict) -> None:
    paths = schema.get("paths", {})
    for path, methods in extensions.get("paths", {}).items():
        path_item = paths.get(path)
        if not isinstance(path_item, dict):
            continue
        for method, operation_extensions in methods.items():
            operation = path_item.get(method.lower())
            if not isinstance(operation, dict) or not isinstance(operation_extensions, dict):
                continue
            operation.update(operation_extensions)


def _merge_root_extensions(schema: dict, extensions: dict) -> None:
    for key, value in extensions.items():
        if key == "paths":
            continue
        schema[key] = value


def build_openapi_schema() -> dict:
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version=app.version,
        openapi_version=app.openapi_version,
        summary=app.summary,
        description=app.description,
        routes=app.routes,
        tags=app.openapi_tags,
        servers=app.servers,
    )
    schema["openapi"] = "3.1.0"
    schema["servers"] = [{"url": MOCK_PROXY_URL}]
    for path in EXCLUDED_PATHS:
        schema.get("paths", {}).pop(path, None)

    extensions = _load_custom_extensions()
    _merge_root_extensions(schema, extensions)
    _merge_operation_extensions(schema, extensions)
    app.openapi_schema = schema
    return schema


def scalar_docs_html(*, openapi_url: str, title: str) -> str:
    return f"""<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title}</title>
  </head>
  <body>
    <div id="app"></div>
    <script id="api-reference" data-url="{openapi_url}"></script>
    <script>
      const configuration = {{
        theme: "deepSpace",
        layout: "modern",
        defaultHttpClient: {{
          targetKey: "python",
          clientKey: "requests",
        }},
        hiddenClients: {{
          c: true,
          clojure: true,
          csharp: true,
          dart: true,
          fsharp: true,
          go: true,
          http: true,
          java: true,
          js: true,
          kotlin: true,
          node: ["axios", "ofetch", "undici"],
          objc: true,
          ocaml: true,
          php: true,
          powershell: true,
          python: ["httpx_async", "httpx_sync", "python3"],
          r: true,
          ruby: true,
          rust: true,
          shell: true,
          swift: true,
        }},
      }};

      const script = document.getElementById("api-reference");
      script.dataset.configuration = JSON.stringify(configuration);
      script.src = "https://cdn.jsdelivr.net/npm/@scalar/api-reference";
    </script>
  </body>
</html>
"""


from app.routes import router as api_router

app.include_router(api_router)
app.openapi = build_openapi_schema


@app.get("/", include_in_schema=False)
async def scalar_docs() -> HTMLResponse:
    return HTMLResponse(scalar_docs_html(openapi_url=app.openapi_url, title=f"{app.title} - Scalar"))


@app.exception_handler(ClientError)
async def unicorn_exception_handler(request: Request, exc: ClientError):
    return JSONResponse(
        status_code=exc.status,
        content={"message": exc.message, "reason": exc.reason},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=3000)
