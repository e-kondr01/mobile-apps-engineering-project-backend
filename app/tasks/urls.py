from rest_framework.routers import DefaultRouter

from .views import SubjectViewSet, TaskViewSet

router = DefaultRouter()
router.register("tasks", TaskViewSet)
router.register("subjects", SubjectViewSet)
urlpatterns = router.urls
