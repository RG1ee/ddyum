from fastapi import HTTPException, status


http_exc_401_unauthorized = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Refused to complete request due to lack of valid authentication.",
)

http_exc_400_bad_email = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="This email is already occupied. Come up with another one.",
)

http_exc_400_bad_data = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Check your email or password.",
)
