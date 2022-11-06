import enum

from rest_framework import serializers

from user.serializers import UserSerializer
from .models import Post


class PostReadSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ("id", "author", "content", "upvote_count", "downvote_count", "created_at", "updated_at")


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("content",)

    def create(self, validated_data):
        return Post.objects.create(
            content=validated_data["content"],
            author=self.context["request"].user
        )


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("content", "upvotes", "downvotes")


class VoteModeEnums:
    UPVOTE = "upvote"
    DOWNVOTE = "downvote"

    CHOICES = [
        (UPVOTE, "upvote"),
        (DOWNVOTE, "downvote"),
    ]


class PostVoteSerializer(serializers.Serializer):
    mode = serializers.ChoiceField(choices=VoteModeEnums.CHOICES)
