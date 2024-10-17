"""naurr app views."""

from typing import Any

from django.conf import settings

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from naurr import __version__
from naurr.serializers import InfoSerializer, UserSerializer


class InfoView(APIView):
    """Return API information."""

    http_method_names = ["get"]
    serializer_class = InfoSerializer

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Return API information."""
        user_serializer = UserSerializer(instance=request.user)

        info = {
            "version": __version__,
            "environment": settings.ENVIRONMENT,
            "user": user_serializer.data,
        }

        info_serializer = self.serializer_class(data=info)
        info_serializer.is_valid(raise_exception=True)

        return Response(info_serializer.data)
