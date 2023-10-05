from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.auth.utils import create_token
from src.base.templates import render_template
from src.config.settings import settings


def create_url_for_confirm(to: str):
    token = create_token(dict(sub=to), settings.EMAIL_TOKEN_EXPIRE)
    url = f"{settings.BASE_URL}{settings.API_PREFIX}/auth/confirm/{token}"

    return url


def preparing_for_email(
    subject: str,
    by: str,
    to: str,
    template_name: str,
    **kwargs,
) -> MIMEMultipart:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = by
    msg["To"] = to
    html = render_template(
        template_name,
        **kwargs,
    )
    part = MIMEText(html, "html")
    msg.attach(part)

    return msg
