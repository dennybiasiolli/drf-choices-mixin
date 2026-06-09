from rest_framework.routers import DefaultRouter

from .views import (
    ArticleViewSet,
    CustomEndpointViewSet,
    CustomKeysViewSet,
    FieldFirstCustomViewSet,
    FieldFirstViewSet,
    FilteredFieldsViewSet,
    ItemViewSet,
    TaskViewSet,
)

router = DefaultRouter()
router.register("tasks", TaskViewSet)
router.register("items", ItemViewSet)
router.register("articles", ArticleViewSet)
router.register("custom-endpoint", CustomEndpointViewSet, basename="custom-endpoint")
router.register("field-first", FieldFirstViewSet, basename="field-first")
router.register(
    "field-first-custom", FieldFirstCustomViewSet, basename="field-first-custom"
)
router.register("filtered", FilteredFieldsViewSet, basename="filtered")
router.register("custom-keys", CustomKeysViewSet, basename="custom-keys")

urlpatterns = router.urls
