from rest_framework.routers import DefaultRouter

from .views import ArticleViewSet, ItemViewSet, TaskViewSet


router = DefaultRouter()
router.register("tasks", TaskViewSet)
router.register("items", ItemViewSet)
router.register("articles", ArticleViewSet)

urlpatterns = router.urls
