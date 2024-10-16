"""filesystem app models."""

from django.db import models

from naurr.utils import BaseModel


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
