import copy
import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import unquote

from fastapi.responses import JSONResponse

from app.models import ClientErrorResponse


DATA_ROOT = Path(__file__).resolve().parents[2] / "data"
TAG_REGEX = re.compile(r"^#2PP+$")
BASE_VARIANT_TAG = "#2PP"
SINGULAR_ITEM_HEADERS = {
    "cache-control": "max-age=600",
    "content-type": "application/json; charset=utf-8",
}

STANDARD_ERROR_RESPONSES = {
    400: {"model": ClientErrorResponse, "description": "Bad request"},
    403: {"model": ClientErrorResponse, "description": "Forbidden"},
    404: {"model": ClientErrorResponse, "description": "Not found"},
    429: {"model": ClientErrorResponse, "description": "Request throttled"},
    500: {"model": ClientErrorResponse, "description": "Unknown exception"},
    503: {"model": ClientErrorResponse, "description": "Maintenance"},
}


def read_wrapped_fixture(relative_path: str) -> dict[str, Any]:
    with (DATA_ROOT / relative_path).open() as fixture_file:
        return json.load(fixture_file)


def _try_read_wrapped_fixture(relative_path: str) -> dict[str, Any] | None:
    try:
        return read_wrapped_fixture(relative_path)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


LOCATIONS_FIXTURE = read_wrapped_fixture("locations/LISTLOCATIONS.json")
LOCATION_ITEMS = LOCATIONS_FIXTURE["body"]["items"]
REGION_LOCATION_IDS = {item["id"] for item in LOCATION_ITEMS if not item["isCountry"]}
COUNTRY_LOCATION_IDS = {item["id"] for item in LOCATION_ITEMS if item["isCountry"]}
LOCATION_BY_ID = {str(item["id"]): item for item in LOCATION_ITEMS}


def normalize_tag(tag: str) -> str:
    return unquote(tag).upper()


def json_response(body: Any, status_code: int = 200, headers: dict[str, str] | None = None) -> JSONResponse:
    response_headers = dict(headers or {})
    response_headers.pop("content-type", None)
    return JSONResponse(status_code=status_code, content=body, headers=response_headers)


def error_response(status_code: int, reason: str, message: str) -> JSONResponse:
    return json_response({"reason": reason, "message": message}, status_code=status_code)


def validate_tag(tag: str) -> tuple[str, JSONResponse | None]:
    normalized_tag = normalize_tag(tag)
    if not TAG_REGEX.fullmatch(normalized_tag):
        return normalized_tag, error_response(
            400,
            "badRequest",
            "Only mock tags in the form #2PP with optional trailing P variants are supported.",
        )
    return normalized_tag, None


def variant_offset(tag: str) -> int:
    return len(tag) - len(BASE_VARIANT_TAG)


def pick_variant(tag: str, variants: list[str]) -> str | None:
    offset = variant_offset(tag)
    if 0 <= offset < len(variants):
        return variants[offset]
    return None


def unsupported_variant_response(tag: str) -> JSONResponse:
    return error_response(400, "badRequest", f"No mock response variant exists for tag '{tag}'.")


def with_limit(body: Any, limit: int | None) -> Any:
    if limit is None or limit < 0:
        return body
    limited_body = copy.deepcopy(body)
    if isinstance(limited_body, dict) and isinstance(limited_body.get("items"), list):
        limited_body["items"] = limited_body["items"][:limit]
    elif isinstance(limited_body, list):
        limited_body = limited_body[:limit]
    return limited_body


def paginate_items_body(body: Any, limit: int | None = None, after: str | None = None, before: str | None = None) -> Any:
    if not isinstance(body, dict) or not isinstance(body.get("items"), list):
        return with_limit(body, limit)

    items = copy.deepcopy(body["items"])
    if limit is None:
        limit = len(items)

    try:
        if after is not None:
            start = int(after)
            if start < 0:
                raise ValueError
        elif before is not None:
            before_index = int(before)
            if before_index < 0:
                raise ValueError
            start = max(0, before_index - limit)
        else:
            start = 0
    except ValueError:
        return error_response(400, "badRequest", "Paging cursors must be numeric offsets.")

    end = min(len(items), start + limit)
    paginated_body = copy.deepcopy(body)
    paginated_body["items"] = items[start:end]
    paginated_body["paging"] = {"cursors": {}}
    if start > 0:
        paginated_body["paging"]["cursors"]["before"] = str(start)
    if end < len(items):
        paginated_body["paging"]["cursors"]["after"] = str(end)
    return paginated_body


def respond_from_fixture(
    relative_path: str,
    *,
    limit: int | None = None,
    after: str | None = None,
    before: str | None = None,
) -> JSONResponse:
    wrapped = copy.deepcopy(_read_wrapped_fixture(relative_path))
    body = wrapped.get("body")
    headers = wrapped.get("headers", {})
    status_code = wrapped.get("response_code", 200)
    body = paginate_items_body(body, limit, after, before)
    if isinstance(body, JSONResponse):
        return body
    return json_response(body, status_code, headers)


def validate_paging(after: str | None, before: str | None) -> JSONResponse | None:
    if after and before:
        return error_response(400, "badRequest", "Only one of 'after' or 'before' can be specified.")
    return None


def location_fixture_name(location_id: str) -> str:
    try:
        location_number = int(location_id)
    except ValueError:
        return "BADREQUEST"
    if location_number in REGION_LOCATION_IDS:
        return "REGION"
    if location_number in COUNTRY_LOCATION_IDS:
        return "COUNTRY"
    return "BADREQUEST"


def fixture_from_location(
    directory: str,
    location_id: str,
    limit: int | None = None,
    after: str | None = None,
    before: str | None = None,
) -> JSONResponse:
    fixture_name = location_fixture_name(location_id)
    return respond_from_fixture(f"locations/{directory}/{fixture_name}.json", limit=limit, after=after, before=before)


def missing_mock_response() -> JSONResponse:
    return respond_from_fixture("errors/MISSING_MOCK.json")


def respond_from_optional_fixture(
    relative_path: str,
    *,
    limit: int | None = None,
    after: str | None = None,
    before: str | None = None,
) -> JSONResponse:
    if _try_read_wrapped_fixture(relative_path) is None:
        return missing_mock_response()
    return respond_from_fixture(relative_path, limit=limit, after=after, before=before)


def respond_item_from_list_fixture(list_path: str, item_id: str, bad_request_path: str | None = None) -> JSONResponse:
    if bad_request_path is not None and not item_id.isdigit():
        return respond_from_fixture(bad_request_path)

    wrapped = _try_read_wrapped_fixture(list_path)
    if wrapped is None:
        return missing_mock_response()

    items = wrapped.get("body", {}).get("items", [])
    for item in items:
        if str(item.get("id")) == item_id:
            return json_response(copy.deepcopy(item), 200, SINGULAR_ITEM_HEADERS)
    if bad_request_path is not None:
        return respond_from_fixture(bad_request_path)
    return error_response(404, "notFound", f"Resource '{item_id}' was not found.")


def lookup_location(location_id: str) -> dict[str, Any] | None:
    return copy.deepcopy(LOCATION_BY_ID.get(location_id))


def replace_item_location(value: Any, location: dict[str, Any]) -> Any:
    if isinstance(value, dict):
        updated = {}
        for key, item in value.items():
            if key == "location" and isinstance(item, dict):
                updated[key] = copy.deepcopy(location)
            else:
                updated[key] = replace_item_location(item, location)
        return updated
    if isinstance(value, list):
        return [replace_item_location(item, location) for item in value]
    return value


def respond_location_rankings_fixture(
    directory: str,
    location_id: str,
    *,
    limit: int | None = None,
    after: str | None = None,
    before: str | None = None,
    rewrite_embedded_location: bool = False,
) -> JSONResponse:
    if location_id == "global":
        return respond_from_fixture(f"locations/{directory}/COUNTRY.json", limit=limit, after=after, before=before)

    location = lookup_location(location_id)
    if location is None:
        return respond_from_fixture(f"locations/{directory}/BADREQUEST.json")

    fixture_name = "COUNTRY" if location.get("isCountry") else "REGION"
    wrapped = copy.deepcopy(read_wrapped_fixture(f"locations/{directory}/{fixture_name}.json"))
    body = paginate_items_body(wrapped.get("body"), limit, after, before)
    if isinstance(body, JSONResponse):
        return body
    if fixture_name == "COUNTRY" and rewrite_embedded_location:
        body = replace_item_location(body, location)
    return json_response(body, wrapped.get("response_code", 200), wrapped.get("headers", {}))


def player_found_payload() -> dict[str, Any]:
    return copy.deepcopy(read_wrapped_fixture("players/player/FOUND.json")["body"])
