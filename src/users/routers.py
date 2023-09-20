from fastapi import APIRouter, Depends, HTTPException, status

from src.users.schemas import UserBaseSchema
from src.auth.dependencies import current_user
from src.users.models import User
from src.users.services import UserService


router = APIRouter(prefix="/users", tags=["User"])


@router.get(
    "/my_profile",
    response_model=UserBaseSchema,
    status_code=status.HTTP_200_OK,
)
async def user_profile(current_user: User = Depends(current_user)):
    user = await UserService.get_one_or_none(id=current_user.id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user
