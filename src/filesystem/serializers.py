"""filesystem app DRF serializers."""

from rest_framework import serializers

from filesystem.models import File, Folder


class FileSerializer(serializers.ModelSerializer):
    """Main DRF serializer for `filesystem.File` model."""

    folder = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Folder.objects.all(),
    )

    class Meta:
        model = File
        fields = ("id", "name", "folder")


class FileNestedSerializer(serializers.ModelSerializer):
    """Nested DRF serializer for `filesystem.File` model."""

    class Meta:
        model = File
        fields = ("id", "name")


class FolderSerializer(serializers.ModelSerializer):
    """Main DRF serializer for `filesystem.Folder` model."""

    files = FileNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Folder
        fields = ("id", "name", "files")
        read_only_fields = ("files",)
