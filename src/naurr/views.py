"""naurr app views."""

from typing import Any

from django.conf import settings

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from naurr import __version__
from naurr.serializers import InfoSerializer


class InfoView(APIView):
    """Return API information."""

    http_method_names = ["get"]

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Return API information."""
        data = {
            "version": __version__,
            "environment": settings.ENVIRONMENT,
            "user": request.user,
        }

        serializer = InfoSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)
