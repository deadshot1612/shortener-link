from django.contrib import admin

from .models import Account, UserConfirmCode

admin.site.register(Account)

admin.site.register(UserConfirmCode)