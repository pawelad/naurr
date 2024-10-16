"""filesystem app DRF serializers."""

from rest_framework import serializers

from filesystem.models import File, Folder


class FolderSerializer(serializers.ModelSerializer):
    """DRF serializer for `filesystem.Folder` model."""

    files = serializers.SlugRelatedField(
        slug_field="name",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Folder
        fields = ("id", "name", "files")
        read_only_fields = ("created_at", "modified_at")


class FileSerializer(serializers.ModelSerializer):
    """DRF serializer for `filesystem.File` model."""

    folder = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Folder.objects.all(),
    )

    class Meta:
        model = File
        fields = ("id", "name", "folder")
        read_only_fields = ("created_at", "modified_at")
