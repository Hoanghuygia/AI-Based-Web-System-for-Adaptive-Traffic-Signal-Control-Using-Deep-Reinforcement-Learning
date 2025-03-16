from fastapi import APIRouter, Depends

from src.models.users import UserInResponse, User
from src.core.jwt import get_current_user_authorizer


router = APIRouter()

@router.get('/user/me', response_model= UserInResponse, tags=['user'])
async def get_current_user(user: User = Depends(get_current_user_authorizer())):
    return UserInResponse(user=user)
