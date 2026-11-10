from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, max_length=128)
    password_confirmation = serializers.CharField(write_only=True, max_length=128)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password", "password_confirmation"]
        extra_kwargs = {
            "email": {"required": True, "max_length": 254},
            "username": {"max_length": 150},
            "first_name": {"required": False, "max_length": 150},
            "last_name": {"required": False, "max_length": 150},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Користувач з таким email вже існує")
        return value

    def validate(self, data):
        if data["password"] != data["password_confirmation"]:
            raise serializers.ValidationError({"password_confirmation": "Паролі не збігаються"})
        return data

    def create(self, validated_data):
        validated_data.pop("password_confirmation")
        return User.objects.create_user(**validated_data)