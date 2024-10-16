"""URL configuration for naurr project."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView
from rest_framework.authtoken.views import obtain_auth_token

api_patterns = (
    [
        # API
        path("", include("filesystem.urls", namespace="filesystem")),
        # Schema and docs
        path("schema/", SpectacularAPIView.as_view(), name="schema"),
        path("docs/", SpectacularRedocView.as_view(url_name="api:schema"), name="docs"),
        # DRF views
        path("auth/", include("rest_framework.urls", namespace="rest_framework")),
        path("auth/obtain_token", obtain_auth_token, name="obtain_token"),
    ],
    "api",
)

urlpatterns = [
    # Django Admin
    path("admin/", admin.site.urls),
    path("api/", include(api_patterns, namespace="api")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
