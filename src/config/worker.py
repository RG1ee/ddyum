from celery import Celery

from src.config.settings import settings


celery = Celery(
    "worker",
    broker=settings.BROKER_URL,
)

celery.autodiscover_tasks(
    ["src.auth.tasks"],
)
