from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, Header, status
from jwt import PyJWTError
from src.controllers.users import get_user_by_username
from src.db.mongodb import AsyncIOMotorClient, get_database
from src.models.token import TokenPayLoad
from src.models.users import User
from starlette.exceptions import HTTPException

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


def _get_authorization_token(authorization: str = Header(...)):
    token_prefix, token = authorization.split(" ")
    if token_prefix != settings.JWT_TOKEN_PREFIX:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authorization type"
        )
    return token


def _get_authorization_token_optional(authorization: str = Header(None)):
    if authorization:
        return _get_authorization_token(authorization)
    return ""


async def _get_current_user(
    conn: AsyncIOMotorClient = Depends(get_database),
    token: str = Depends(_get_authorization_token),
) -> User:
    try:
        payload = jwt.decode(token, str(settings.SECRET_KEY), algorithms=[ALGORITHM])
        token_data = TokenPayLoad(**payload)
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials.",
        )

    db_user = await get_user_by_username(conn, token_data.username)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    user = User(**db_user.model_dump(), token=token)
    return user


async def get_current_user_optional(
    db: AsyncIOMotorClient = Depends(get_database),
    token: str = Depends(_get_authorization_token_optional),
) -> User | None:
    if token:
        return await _get_current_user(db, token)
    return None


def get_current_user_authorizer(*, required: bool = True):
    if required:
        return _get_current_user
    else:
        return get_current_user_optional
