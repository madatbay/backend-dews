from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("author", "upvote_count", "downvote_count", "created_at", "updated_at")
    list_filter = ("author", "created_at", "updated_at")
    search_fields = ("content",)
