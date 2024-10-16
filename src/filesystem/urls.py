"""filesystem app URLs configuration."""

from rest_framework.routers import DefaultRouter

from filesystem import views

router = DefaultRouter()
router.register("folder", views.FolderViewSet, basename="folder")
router.register("file", views.FileViewSet, basename="file")

app_name = "filesystem"
urlpatterns = router.urls
