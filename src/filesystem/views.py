"""filesystem app DRF views."""

from typing import Any

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from filesystem.models import File, Folder
from filesystem.serializers import FileSerializer, FolderSerializer


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
        grouped_values = request.data

        saved_folders, saved_files = Folder.save_from_grouped_values(grouped_values)

        data = {
            "saved_folders": saved_folders,
            "saved_files": saved_files,
        }

        return Response(data, status=status.HTTP_201_CREATED)


class FileViewSet(viewsets.ModelViewSet):
    """CRUD viewset for `File` model.

    It allows listing, retrieving, creating, updating and deleting the objects.
    """

    queryset = File.objects.select_related("folder").all()
    serializer_class = FileSerializer
