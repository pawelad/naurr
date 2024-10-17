"""filesystem app DRF views."""

from typing import Any

import pydantic
from drf_spectacular.utils import extend_schema, extend_schema_view, inline_serializer
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.fields import IntegerField
from rest_framework.request import Request
from rest_framework.response import Response

from filesystem.models import File, Folder
from filesystem.serializers import FileSerializer, FolderBulkAddSchema, FolderSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List folders",
        description="List all available folders and their files.",
    ),
    create=extend_schema(
        summary="Create a folder",
        description="Create a new folder.",
    ),
    retrieve=extend_schema(
        summary="Retrieve a folder",
        description="Retrieve existing folder details.",
    ),
    update=extend_schema(
        summary="Update a folder",
        description="Update an existing folder.",
    ),
    partial_update=extend_schema(
        summary="Partially update a folder",
        description="Partially update an existing folder.",
    ),
    destroy=extend_schema(
        summary="Delete a folder",
        description="Delete a folder. It must be empty to succeed.",
    ),
    bulk_add=extend_schema(
        summary="Bulk add folders and nested files",
        description=(
            "Bulk add folders and nested files. The input format should be a single "
            "nested dictionary, where the key is the (unique) name of the group, "
            "and the value is a list of file names."
        ),
        request=FolderBulkAddSchema,
        responses={
            "201": inline_serializer(
                "SavedFoldersInfo",
                {"saved_folders": IntegerField(), "saved_files": IntegerField()},
            )
        },
    ),
)
class FolderViewSet(viewsets.ModelViewSet):
    """CRUD viewset for `Folder` model.

    It allows listing, retrieving, creating, updating and deleting the objects.
    """

    queryset = Folder.objects.prefetch_related("files").all()
    serializer_class = FolderSerializer

    @action(detail=False, methods=["post"])
    def bulk_add(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Import folders and nested files from passed data.

        The input format should be a single nested dictionary, where the key is
        the (unique) name of the group, and the value is a list of file names.
        """
        try:
            grouped_values = FolderBulkAddSchema(request.data)
        except pydantic.ValidationError as e:
            errors_data: Any = e.errors()
            raise ValidationError({"errors": errors_data}) from e

        saved_folders, saved_files = Folder.save_from_grouped_values(
            grouped_values.model_dump()
        )

        data = {
            "saved_folders": saved_folders,
            "saved_files": saved_files,
        }

        return Response(data, status=status.HTTP_201_CREATED)


@extend_schema_view(
    list=extend_schema(
        summary="List files",
        description="List all available files.",
    ),
    create=extend_schema(
        summary="Create a file",
        description="Create a new file.",
    ),
    retrieve=extend_schema(
        summary="Retrieve a file",
        description="Retrieve existing file details.",
    ),
    update=extend_schema(
        summary="Update a file",
        description="Update an existing file.",
    ),
    partial_update=extend_schema(
        summary="Partially update a file",
        description="Partially update an existing file.",
    ),
    destroy=extend_schema(
        summary="Delete a file",
        description="Delete a file.",
    ),
)
class FileViewSet(viewsets.ModelViewSet):
    """CRUD viewset for `File` model.

    It allows listing, retrieving, creating, updating and deleting the objects.
    """

    queryset = File.objects.select_related("folder").all()
    serializer_class = FileSerializer
