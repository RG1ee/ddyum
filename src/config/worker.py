from celery import Celery

from src.config.settings import settings


celery = Celery(
    "worker",
    broker=f"{settings.BROKER_DSN}",
)

celery.autodiscover_tasks(
    ["src.tasks"],
)
