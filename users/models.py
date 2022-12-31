from django.db import models
from django.contrib.auth.models import AbstractUser
from Mixins.mixins import DateTimeMixin


class User(AbstractUser):
    nationality = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    phone_is_verified = models.BooleanField(default=False)
    email_is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
