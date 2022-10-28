import os

from django.db import models
from django.contrib.auth.models import AbstractUser


def get_upload_path(instance, filename):
    return os.path.join(
        "user_%d" % instance.id, instance.__class__.__name__, filename)


class User(AbstractUser):
    profile_photo = models.ImageField(upload_to=get_upload_path, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
