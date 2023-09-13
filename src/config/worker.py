from celery import Celery

from src.config.settings import settings


celery = Celery(
    "worker",
    broker=settings.BROKER_URL,
    include=["src.tasks.tasks"],
)
