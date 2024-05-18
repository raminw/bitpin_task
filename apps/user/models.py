from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.user.managers import UserManager
from apps.common.model_mixins import TimeMixin


class User(TimeMixin, AbstractUser):
    objects = UserManager()

    first_name = models.CharField(max_length=150, null=True)
    last_name = models.CharField(max_length=150, null=True)
    birthday = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['id']
        db_table = 'auth_user'
