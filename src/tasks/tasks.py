from src.config.worker import celery


@celery.task
def test_task():
    print("Test Task")
