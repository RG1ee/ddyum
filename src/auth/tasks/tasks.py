import smtplib

from src.config.worker import celery
from src.config.settings import settings
from src.auth.email_utils import preparing_for_email


@celery.task
def send_user_verification_email(user_email: str):
    with smtplib.SMTP_SSL(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
        msg = preparing_for_email(
            settings.SUBJECT,
            settings.SMTP_LOGIN,
            user_email,
        )
        server.login(settings.SMTP_LOGIN, settings.SMTP_PASSWORD)
        server.sendmail(settings.SMTP_LOGIN, user_email, msg=msg.as_string())
