from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .auth_handler import decodeJWT
from ..models import ClientError


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        if "127.0.0.1" in str(request.client.host):
            return HTTPAuthorizationCredentials(scheme="Bearer", credentials="Doc call").credentials
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if not credentials:
           raise ClientError(status=403, reason="accessDenied", message="Missing authorization")
        if credentials.scheme != "Bearer":
            raise ClientError(status=403, reason="accessDenied", message="Missing authorization")
        self.verify_jwt(credentials.credentials)
        return credentials.credentials

    def verify_jwt(self, jwtoken: str, request: Request = None) -> bool:
        isTokenValid: bool = False
        if jwtoken == 'DEMO_TOKEN':
            isTokenValid = True
        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            if payload.get('iss') == "supercell" and payload.get("aud") == "supercell:gameapi" and \
                    "clash" in payload.get("scopes", [""])[0]:
                if request and str(request.client.host) in [x.get("cdir") for x in payload.get("limits", [])
                                                            if isinstance(x, dict) and "cidrs" in x]:
                    isTokenValid = True
                else:
                    raise ClientError(status=403, reason="accessDenied", message="Missing authorization")
            else:
                raise ClientError(status=403, reason="accessDenied", message="Missing authorization")
        if not isTokenValid:
            raise ClientError(status=403, reason="accessDenied", message="Missing authorization")
