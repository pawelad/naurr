"""filesystem app models."""

from typing import NamedTuple

from django.db import models

from naurr.utils import BaseModel


class FolderSavedCount(NamedTuple):
    """Container for keeping track of saved folders and files count."""

    folder_saved_count: int
    file_saved_count: int


class Folder(BaseModel):
    """Folder (directory / group) model representation."""

    name = models.CharField(
        verbose_name="name",
        max_length=255,
        blank=False,
        help_text="Folder name",
    )

    class Meta:
        verbose_name = "folder"
        verbose_name_plural = "folders"
        constraints = [
            models.UniqueConstraint(fields=["name"], name="unique_name"),
        ]

    @staticmethod
    def save_from_grouped_values(
        grouped_values: dict[str, list[str]]
    ) -> FolderSavedCount:
        """Helper method to save folders and nested files from passed dictionary.

        Arguments:
            grouped_values: File names grouped into folders (no nested structures).

        Returns:
            Number of saved folders and files.
        """
        folder_saved_count = 0
        file_saved_count = 0

        for folder_name, folder_files in grouped_values.items():
            folder, created = Folder.objects.update_or_create(name=folder_name)
            if created:
                folder_saved_count += 1

            for file_name in folder_files:
                _, created = File.objects.update_or_create(
                    name=file_name,
                    folder=folder,
                )
                if created:
                    file_saved_count += 1

        return FolderSavedCount(folder_saved_count, file_saved_count)

    def __str__(self) -> str:
        """Return a human-readable folder name."""
        return f"{self.name} (ID: {self.pk})"


class File(BaseModel):
    """File (that belongs to a folder) model representation."""

    folder = models.ForeignKey(
        verbose_name="folder",
        to="filesystem.Folder",
        related_name="files",
        # TODO: Should deleting a folder with files inside delete them implicitly?
        on_delete=models.PROTECT,
    )

    name = models.CharField(
        verbose_name="name",
        max_length=255,
        blank=False,
        help_text="File name",
    )

    class Meta:
        verbose_name = "file"
        verbose_name_plural = "files"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "folder"], name="unique_name_folder"
            ),
        ]

    def __str__(self) -> str:
        """Return a human-readable file name."""
        return f"{self.folder.name}/{self.name} (ID: {self.pk})"
