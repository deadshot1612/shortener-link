from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from account.manager import UserManager



class Account(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=15)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    staff = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    bio = models.CharField(max_length=800)
    profile_photo = models.ImageField(upload_to='media/avatars/', null=True, default='media/avatar/ava.png')
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_perms(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser