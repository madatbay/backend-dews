from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

from user.models import FollowRelation

User = get_user_model()


class FollowRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowRelation
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()
    last_login = serializers.ReadOnlyField()
    followings = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    profile_photo = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "profile_photo", "first_name", "last_name", "bio", "birth_date", "location", "username", "email",
            "date_joined", "last_login", "followings", "followers")

    def get_profile_photo(self, user: User):
        request = self.context["request"]
        if user.profile_photo:
            photo_url = user.profile_photo.url
            return request.build_absolute_uri(photo_url)

    def get_followings(self, user: User):
        return FollowRelationSerializer(user.followings.all(), many=True).data

    def get_followers(self, user: User):
        return FollowRelationSerializer(user.followers.all(), many=True).data


class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    username = serializers.CharField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "password2", "first_name", "last_name")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            username=validated_data["username"],
            email=validated_data["email"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user
