from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import get_object_or_404

from .utils import get_tokens_for_user

User = get_user_model()


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "uid",
            "first_name",
            "last_name",
            "username",
            "email",
            "date_joined",
            "last_login",
            "user_type",
            "password",
        ]

        read_only_fields = ("date_joined", "last_login")

    def create(self, validated_data, *args, **kwargs):
        password = validated_data["password"]

        user = User.objects.create(
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            username=validated_data["username"],
            email=validated_data["email"].lower(),
            user_type=validated_data.get("user_type", ""),
        )
        user.set_password(password)
        user.save()
        return validated_data


class UserAccountLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)

    def create(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.get("password")
        user = get_object_or_404(User.objects.filter(), email=email)

        if not user.check_password(password):
            raise AuthenticationFailed(detail="Invalid credentials.")

        if not user:
            raise AuthenticationFailed(
                detail="Invalid credentials."
            )

        # Get JWT tokens
        tokens = get_tokens_for_user(user)
        validated_data["refresh"] = tokens["refresh"]
        validated_data["access"] = tokens["access"]

        return validated_data


class PrivateUserProfile(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            "uid",
            "first_name",
            "last_name",
            "username",
            "email",
            "user_type",
            "date_joined",
            "last_login",
            "password",
        ]

        read_only_fields = ("date_joined", "last_login")

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password:
            validated_data["password"] = make_password(password)
        return super().update(instance, validated_data)
