"""URL configuration for naurr project."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from rest_framework.authtoken import views as authtoken_views

urlpatterns = [
    # Django Admin
    path("admin/", admin.site.urls),
    # API
    path(
        "api/",
        include(
            [
                # DRF views
                path(
                    "auth/",
                    include("rest_framework.urls", namespace="rest_framework"),
                ),
                path(
                    "auth/obtain_token",
                    authtoken_views.obtain_auth_token,
                    name="obtain_token",
                ),
                # API
                path("", include("filesystem.urls", namespace="filesystem")),
            ]
        ),
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
