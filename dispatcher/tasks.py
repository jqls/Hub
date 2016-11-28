from celery.app import shared_task


@shared_task
def plus(a, b):
    return a + b
