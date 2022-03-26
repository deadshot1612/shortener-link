from celery import Celery
from django.conf import settings
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('shortener-link')



app.config_from_object('django.conf:settings')
app.autodiscover_tasks(settings.INSTALLED_APPS)