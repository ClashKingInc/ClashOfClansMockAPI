from datetime import datetime, timedelta
from typing import Dict, Optional

import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel



def decodeJWT(token: str) -> dict:
    try:
        return jwt.decode(token, algorithms=["HS512"])
    except:
        return {}
