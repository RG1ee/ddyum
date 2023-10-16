from fastapi import HTTPException, status


http_exc_401_unauthorized = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Refused to complete request due to lack of valid authentication.",
    headers={"WWW-Authenticate": "Bearer"},
)

http_exc_400_bad_email = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="This email is already occupied. Come up with another one.",
)

http_exc_400_bad_data = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="The user is not found, check the correctness of the email and password",
)

http_exc_409_conflict = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail=(
        "Sorry, you already have an active reservation. "
        "Please cancel it if you have chosen another day or another service."
    ),
)

http_exc_404_booking_type_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Booking Type not found."
)
