import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'WeeklyNewsletter': {
        'task': 'app.tasks.weekly_newsletter',
        'schedule': crontab(hour=8, day_of_week='monday'),
        'args': (),
    },
    'cleanup_codes': {
        'task': 'app.tasks.cleanup_codes',
        'schedule': crontab(minute='*/3'),
    },
}
