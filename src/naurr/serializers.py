"""naurr app serializers."""

from django.contrib.auth.models import User

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Django user serializer."""

    class Meta:
        model = User
        fields = ("username", "email", "is_staff", "is_superuser")
        read_only_fields = fields


class InfoSerializer(serializers.Serializer):
    """Simple API info serializer."""

    version = serializers.CharField()
    environment = serializers.CharField()
    user = serializers.DictField()

    class Meta:
        fields = ("version", "environment", "user")
        read_only_fields = fields
