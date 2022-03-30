from django.db import models
from django.utils import timezone
from account.models import Account

# Create your models here.
from short_link.utils import create_shortened_url

class Shortener(models.Model):
    user = models.ForeignKey(Account,null=True, on_delete=models.CASCADE)
    used = models.DateField(default=timezone.now)
    long_url = models.URLField()
    short_url = models.CharField(max_length=5, unique=True, blank=True)


    def __str__(self):

        return f'{self.long_url} to {self.short_url}'\

    def save(self, *args, **kwargs):
        if not self.short_url:
            self.short_url = create_shortened_url(self)
        super().save(*args, **kwargs)