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


class FollowRelation(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followings")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["from_user", "to_user"]

    def __str__(self):
        return f"FollowRelation({self.id}): {self.from_user}->{self.to_user}"

    def __repr__(self):
        _class = type(self)
        return "%s(id=%r, from=%r, to=%r)" % (
            _class.__name__,
            self.id,
            self.from_user.email,
            self.to_user.email,
        )
