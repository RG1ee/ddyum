import pytest

from src.auth.tasks.tasks import send_user_verification_email
from src.config.settings import settings


@pytest.mark.parametrize(
    "user_email",
    [
        ("newuser@test.com"),
        ("newuser2@test.com"),
    ],
)
def test_send_email(mocker, user_email: str):
    mock_SMTP = mocker.MagicMock(name="smtp_mock")
    mocker.patch("smtplib.SMTP_SSL", new=mock_SMTP)

    send_user_verification_email(user_email)

    expected_args = (settings.SMTP_SERVER, settings.SMTP_PORT)
    mock_SMTP.assert_called_once_with(*expected_args)
