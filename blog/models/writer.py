from django.db import models
from django.contrib.auth import get_user_model


class Writer(models.Model):
    name = models.CharField(max_length=63)
    is_editor = models.BooleanField(default=True)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
