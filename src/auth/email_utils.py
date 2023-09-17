from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.auth.utils import create_token
from src.config.settings import settings


def preparing_for_email(
    subject: str,
    by: str,
    to: str,
) -> MIMEMultipart:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = by
    msg["To"] = to
    text = f"{settings.BASE_URL}/auth/confirm/{create_token(dict(sub=to), 60 * 60)}"
    part = MIMEText(text, "plain")
    msg.attach(part)

    return msg
