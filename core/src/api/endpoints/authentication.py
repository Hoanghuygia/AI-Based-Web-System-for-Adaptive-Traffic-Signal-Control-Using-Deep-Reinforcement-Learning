from datetime import timedelta

from fastapi import APIRouter, Body, Depends, status

from src.models.users import User, UserInLogin, UserInResponse
from src.controllers.users import create_user
from src.core.config import settings
from src.core.jwt import create_access_token
from src.db.mongodb import AsyncIOMotorClient, get_database

router = APIRouter()

@router.post(
    "/users",
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
            token = create_access_token(
                data={"username": db_user.username},
                expires_delta=access_token_expiration,
            )
            return UserInResponse(user=User(**db_user.model_dump(), token=token))
