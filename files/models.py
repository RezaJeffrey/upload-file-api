from django.db import models
from Mixins.mixins import DateTimeMixin
from django.contrib.auth import get_user_model

User = get_user_model()


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<username>/<filename>
    return f'user_{instance.user.username}/{filename}'


class File(DateTimeMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=40, blank=True, null=True)
    file = models.FileField(upload_to=user_directory_path)

    def __str__(self):
        if self.title:
            return f'{self.user.username} - {self.title}'
        else:
            return f'{self.user.username} - {self.pk}'

    def file_username(self):
        return self.user.username
