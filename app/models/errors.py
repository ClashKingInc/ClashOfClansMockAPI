
from typing import Any

from .common import ApiModel


class ClientErrorResponse(ApiModel):
    reason: str
    message: str
    type: str | None = None
    detail: dict[str, Any] | None = None


class VerifyTokenRequest(ApiModel):
    token: str


class VerifyTokenResponse(ApiModel):
    tag: str
    token: str
    status: str
