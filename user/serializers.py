from rest_framework import serializers
from user.models import Writer, Task, Project, Client, SubmitTask
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

User = get_user_model()

from typing import Any

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):  
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

class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ["email"]


class WriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Writer
        fields = ["id", "name", "specialization", "date", "email", "phone_number"]


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class FullNameToUserSerializer(serializers.Serializer):
    """
    Serializer field that converts full name to User object.
    """

    def to_internal_value(self, data):
        # Check if data is empty or does not contain a space-separated full name
        if not data or ' ' not in data:
            raise serializers.ValidationError("Invalid full name format.")
        
        # Assuming the full name is in the format "first_name last_name"
        first_name, last_name = data.split(" ", 1)
        try:
            user = User.objects.get(first_name=first_name, last_name=last_name)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with the provided full name does not exist.")
        return user

    def to_representation(self, value):
        return f"{value.first_name} {value.last_name}"

class TaskSerializer(serializers.ModelSerializer):
    writer = FullNameToUserSerializer()

    class Meta:
        model = Task
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class SubmitTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmitTask
        fields = "__all__"
