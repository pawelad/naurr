"""filesystem app Django Admin integration."""

from django.contrib import admin

from filesystem.models import File, Folder


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    """Django Admin integration for `filesystem.Folder` model."""

    list_display = (
        "pk",
        "name",
        "files",
        "created_at",
        "modified_at",
    )

    list_filter = (
        "created_at",
        "modified_at",
    )

    ordering = (
        # "files",
        "modified_at",
        "created_at",
    )

    search_fields = ("name",)

    # TODO: Why does adding `ordering=Count("files")` cause item duplication?
    @admin.display(description="Number of files", ordering="files_count")
    def files(self, obj: Folder) -> str:
        """Return the count of files in passed folder."""
        return str(obj.files.count())


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    """Django Admin integration for `filesystem.File` model."""

    list_display = (
        "pk",
        "name",
        "folder",
        "created_at",
        "modified_at",
    )

    list_filter = (
        "folder",
        "created_at",
        "modified_at",
    )

    ordering = (
        "modified_at",
        "created_at",
    )

    search_fields = (
        "name",
        "folder",
    )
