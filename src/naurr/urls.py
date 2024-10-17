"""URL configuration for naurr project."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import URLPattern, URLResolver, include, path
from django.views.generic import RedirectView

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView
from rest_framework.authtoken.views import obtain_auth_token

from naurr.views import InfoView

api_patterns: list[URLPattern | URLResolver] = [
    # API
    path("info", InfoView.as_view(), name="info"),
    path("", include("filesystem.urls", namespace="filesystem")),
    # Schema and docs
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularRedocView.as_view(url_name="api:schema"), name="docs"),
]


urlpatterns = [
    path("", RedirectView.as_view(pattern_name="api:docs")),
    # API
    path("api/", include((api_patterns, "api"), namespace="api")),
    # DRF views (need to be outside of `api` namespace)
    path("api/auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/auth/obtain_token", obtain_auth_token, name="obtain_token"),
    # Django Admin
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
