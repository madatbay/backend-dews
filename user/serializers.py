from django.contrib.auth.password_validation import validate_password
from django.utils import timezone

from rest_framework import serializers

from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()
    last_login = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "date_joined", "last_login")


class RegisterSerializer(serializers.ModelSerializer):
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
            full_name=validated_data["full_name"],
            username=validated_data["username"],
            email=validated_data["email"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user
