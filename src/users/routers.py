from fastapi import APIRouter, HTTPException, status

from src.users.schemas import UserRegistrationSchema
from src.users.services import UserService
from src.users.utils import create_hash_password


router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    path="/register",
    status_code=status.HTTP_201_CREATED,
)
async def registration_user(payload: UserRegistrationSchema) -> dict:
    existing_user = await UserService.get_one_or_none(email=payload.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    hashed_password = create_hash_password(payload.password)
    await UserService.insert_data(
        email=payload.email,
        hashed_password=hashed_password,
    )
    return dict(email=payload.email)
