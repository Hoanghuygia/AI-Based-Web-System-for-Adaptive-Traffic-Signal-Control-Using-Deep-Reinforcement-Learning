from datetime import timedelta

import jwt
from fastapi import APIRouter, Body, Depends, HTTPException, status
from jwt import PyJWTError
from src.controllers.users import create_user, get_user_by_username
from src.core.config import settings
from src.core.jwt import create_access_token, create_token, get_current_user_authorizer
from src.db.mongodb import AsyncIOMotorClient, get_database
from src.models.token import RefreshTokenRequest, TokenResponse
from src.models.users import User, UserInLogin, UserInResponse

router = APIRouter()


@router.post(
    "/refresh",
    response_model=TokenResponse,
    tags=["authentication"],
    status_code=status.HTTP_202_ACCEPTED,
)
async def refresh_access_token(data: RefreshTokenRequest):
    try:
        payload = jwt.decode(
            data.refresh_token, str(settings.SECRET_KEY), algorithms=["HS256"]
        )

        if not payload.get("refresh"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Refresh token is missing"
            )

        username = payload.get("username")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Username is missing"
            )

        new_access_token_expiration = timedelta(
            minutes=settings.ACCESSS_TOKEN_EXPIRED_TIME
        )
        new_access_token = create_token(
            data={"username": username}, expires_delta=new_access_token_expiration
        )

        return TokenResponse(
            access_token=new_access_token, refresh_token=data.refresh_token
        )

    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Can not verify refresh token"
        )


@router.post("/logout", tags=["authentication"], status_code=status.HTTP_202_ACCEPTED)
async def logout(user: User = Depends(get_current_user_authorizer())):
    return {
        "details": "Logget out, please remove access token and refresh token at client side."
    }


@router.post(
    "/login",
    response_model=UserInResponse,
    tags=["authentication"],
    status_code=status.HTTP_201_CREATED,
)
async def login(
    user: UserInLogin = Body(..., embed=True),
    db: AsyncIOMotorClient = Depends(get_database),
):
    db_user = await get_user_by_username(db, user.username)
    if not db_user or not db_user.check_password(user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )

    access_token_expiration = timedelta(minutes=settings.ACCESSS_TOKEN_EXPIRED_TIME)
    access_token = create_token(
        data={"username": user.username}, expires_delta=access_token_expiration
    )

    refresh_token_expiration = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRED_TIME)
    refresh_token = create_token(
        data={"username": user.username, "refresh": True},
        expires_delta=refresh_token_expiration,
    )

    return UserInResponse(
        user=User(
            **db_user.model_dump(), token=access_token, refresh_token=refresh_token
        )
    )


@router.post(
    "/register",
    response_model=UserInResponse,
    tags=["authentication"],
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user: UserInLogin = Body(
        ...,
        embedded=True,
    ),
    db: AsyncIOMotorClient = Depends(get_database),
):
    async with await db.start_session() as session:
        async with session.start_transaction():
            db_user = await create_user(db, user)
            access_token_expiration = timedelta(
                minutes=settings.ACCESSS_TOKEN_EXPIRED_TIME
            )
            token = create_token(
                data={"username": db_user.username},
                expires_delta=access_token_expiration,
            )
            return UserInResponse(user=User(**db_user.model_dump(), token=token))
