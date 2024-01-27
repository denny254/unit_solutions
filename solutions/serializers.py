from rest_framework import serializers
from solutions.models import Writer, Task, Project, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers


User = get_user_model()

from typing import Any

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):  # type: ignore
    @classmethod
    def get_token(cls, user: Any) -> Any:
        token = super().get_token(user)
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        token["email"] = user.email
        token["user_group"] = user.user_group
        token["username"] = user.username
        return token


class NewPasswordSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords must match.")
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, value: str):
        """
        User password validation.

        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long."
            )
        if value.isalpha():
            raise serializers.ValidationError(
                "Password must contain at least one number."
            )
        if value.isnumeric():
            raise serializers.ValidationError(
                "Password must contain at least one letter."
            )
        if value.islower():
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter."
            )
        if value.isupper():
            raise serializers.ValidationError(
                "Password must contain at least one lowercase letter."
            )
        if value.isalnum():
            raise serializers.ValidationError(
                "Password must contain at least one special character."
            )
        return make_password(value)


class WriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Writer
        fields = ["id", "name", "specialization", "date", "email", "phone_number"]


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "status", "writer", "book_balance", "deadline"]


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
