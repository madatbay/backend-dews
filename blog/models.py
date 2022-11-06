from django.db import models

from user.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(blank=True, null=True)
    upvotes = models.ManyToManyField(User, blank=True, related_name="upvotes")
    downvotes = models.ManyToManyField(User, blank=True, related_name="downvotes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Post: {self.id}-{self.author.email}"

    def __repr__(self):
        _class = type(self)
        return "%s(id=%r, author=%r)" % (
            _class.__name__,
            self.id,
            self.author_id
        )

    @property
    def upvote_count(self):
        return self.upvotes.count()

    @property
    def downvote_count(self):
        return self.downvotes.count()
