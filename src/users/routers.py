from fastapi import APIRouter, Depends, status

from src.auth.dependencies import current_user
from src.users.models import User
from src.users.services import ProfileService, UserService
from src.users.schemas import ProfileSchema, UpdateProfileSchema


router = APIRouter(prefix="/users", tags=["User"])


@router.get(
    "/my_profile",
    status_code=status.HTTP_200_OK,
    response_model=ProfileSchema,
)
async def user_profile(current_user: User = Depends(current_user)):
    user = await UserService.get_user_with_profile(current_user.id)
    return user


@router.patch(
    "/my_profile/update",
    status_code=status.HTTP_200_OK,
    response_model=UpdateProfileSchema,
)
async def profile_update(
    payload: UpdateProfileSchema,
    current_user: User = Depends(current_user),
):
    updated_data = await ProfileService.update_data(
        current_user.id, **payload.model_dump(exclude_unset=True)
    )
    return updated_data
