from celery import Celery
from celery.schedules import crontab
from app.core.config import settings

celery_app = Celery(
    'social_bot',
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=['app.tasks.follower_tasks']
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

celery_app.conf.beat_schedule = {
    'check-follower-counts': {
        'task': 'app.tasks.follower_tasks.check_all_profiles',
        'schedule': crontab(minute='*/5'),  # Run every 5 minutes
    },
}
