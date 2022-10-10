from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CompleteTaskView, SubjectViewSet, TaskViewSet

router = DefaultRouter()
router.register("tasks", TaskViewSet)
router.register("subjects", SubjectViewSet)

urlpatterns = [
    path(
        "tasks/<int:pk>/completion/",
        CompleteTaskView.as_view(),
    )
]

urlpatterns += router.urls
