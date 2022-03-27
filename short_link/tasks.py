from datetime import timedelta
from celery import shared_task
from django.utils import timezone

from short_link.models import Shortener



@shared_task
def check_urls_status():
    for link_status in Shortener.objects.all():
        time_now = timezone.now()
        if time_now > link_status.used + timedelta(days=2):
            link_status.delete()
