from django.conf import settings
from django.db import models


class Writer(models.Model):
    name = models.CharField(max_length=64)
    is_editor = models.BooleanField(default=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='writer_profile')
