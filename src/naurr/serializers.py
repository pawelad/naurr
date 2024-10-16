"""naurr app serializers."""

from django.contrib.auth.models import User

from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    """Django user serializer."""

    class Meta:
        model = User
        fields = ("pk", "username", "email", "is_active", "is_staff", "is_superuser")


class InfoSerializer(serializers.Serializer):
    """Simple API info serializer."""

    version = serializers.CharField()
    environment = serializers.CharField()
    user = UserSerializer()
