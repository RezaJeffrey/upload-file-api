from django.db import models


class DateTimeMixin(models.Model):
    created_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True
