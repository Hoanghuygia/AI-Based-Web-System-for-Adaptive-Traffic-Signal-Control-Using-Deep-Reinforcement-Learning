from datetime import datetime, timedelta, timezone
import jwt

from .config import settings

ALGORITHM = "HS256"
access_token_jwt_subject = "access"

def create_access_token(*, data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire, "sub": access_token_jwt_subject})
    encoded_jwt = jwt.encode(to_encode, str(settings.SECRET_KEY), algorithm=ALGORITHM)
    return encoded_jwt
