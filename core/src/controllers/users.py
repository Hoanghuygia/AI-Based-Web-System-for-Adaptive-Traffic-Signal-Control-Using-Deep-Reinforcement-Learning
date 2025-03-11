from bson.objectid import ObjectId
from fastapi import HTTPException, status

from ..core.config import settings
from ..db.mongodb import AsyncIOMotorClient
from ..models.users import UserInDB, UserInLogin

# async def check_free_username(
#         conn: AsyncIOMotorClient, username: str | None  = None
# ):
#     if username:
#         user_by_username = await get_user(conn, username)
#         if user_by_username:
#             raise HTTPException(
#                 status_code=HTTP_422_UNPROCESSABLE_ENTITY,
#                 detail="User with this username already exists",
#             )
#     if email:
#         user_by_email = await get_user_by_email(conn, email)
#         if user_by_email:
#             raise HTTPException(
#                 status_code=HTTP_422_UNPROCESSABLE_ENTITY,
#                 detail="User with this email already exists",
#             )


async def get_user_by_username(conn: AsyncIOMotorClient, username: str) -> UserInDB:
    user = await conn[settings.DB_NAME][settings.USER_COLLECTION_NAME].find_one(
        {"username": username}
    )
    if user:
        user["_id"] = str(user["_id"])
        return UserInDB(**user)


async def create_user(conn: AsyncIOMotorClient, user: UserInLogin) -> UserInDB:
    existing_user = await conn[settings.DB_NAME][
        settings.USER_COLLECTION_NAME
    ].find_one({"username": user.username})

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered"
        )

    db_user = UserInDB(**user.model_dump())
    db_user.change_password(user.password)

    row = await conn[settings.DB_NAME][settings.USER_COLLECTION_NAME].insert_one(
        db_user.model_dump(exclude={"id"})
    )

    db_user.id = row.inserted_id
    db_user.created_at = ObjectId(db_user.id).generation_time
    db_user.updated_at = ObjectId(db_user.id).generation_time

    return db_user
