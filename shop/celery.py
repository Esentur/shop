import os
import django
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')
django.setup()
app = Celery('shop')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
# создаем спамера
app.conf.beat_schedule = {
    'send_spam_from_john': {
        'task': 'apps.account.tasks.celery_spam_email',
        'schedule': crontab(minute='*/1')
    },
    'send_spam_from_todo': {
        'task': 'apps.spam.tasks.celery_spam_todo',
        'schedule': crontab(minute='*/1')
    }
}
# celery -A shop beat перед стартом в новом терминале
