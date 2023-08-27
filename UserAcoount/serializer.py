from rest_framework import serializers

from .models import User

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
            "password"
        ]

        read_only_fields = ("date_joined","last_login")

    
    def create(self, validated_data, *args, **kwargs):
        first_name = validated_data["first_name"]
        last_name = validated_data["last_name"]
        username = validated_data["username"]
        user_type = validated_data["user_type"]
        email = validated_data["email"].lower()
        password = validated_data["password"]

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            user_type=user_type
        )
        user.set_password(password)
        user.save()
        return validated_data
