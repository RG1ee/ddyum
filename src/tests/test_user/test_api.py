# from httpx import AsyncClient
# import pytest

# from src.config.settings import settings


# @pytest.mark.parametrize(
#     "user_id, email, telegram, phone, status",
#     [
#         (1, "test@test.com", "test", "88003333333", 200),
#     ],
# )
# async def test_get_user_profile(
#     client: AsyncClient,
#     authenticated_client: AsyncClient,
#     user_id: int,
#     email: str,
#     telegram: str,
#     phone: str,
#     status: int,
# ):
#     response = await authenticated_client.get(f"{settings.API_PREFIX}/users/my_profile")

#     assert response.json() == {
#         "id": user_id,
#         "email": email,
#         "telegram": telegram,
#         "phone": phone,
#     }
#     assert response.status_code == status

#     response = await client.get(f"{settings.API_PREFIX}/users/my_profile")
#     assert response.status_code == 401
