from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, FollowRelation


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info",
         {"fields": (
             "profile_photo", "first_name", "last_name", "email", "bio", "birth_date", "location")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )


@admin.register(FollowRelation)
class FollowRelationAdmin(admin.ModelAdmin):
    pass
