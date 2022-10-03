from django.utils import timezone
from rest_framework.viewsets import ModelViewSet

from .models import Subject, Task
from .serializers import SubjectSerializer, TaskDetailSerializer, TaskListSerializer


class TaskViewSet(ModelViewSet):
    """
    CRUD для задач.
    """

    queryset = Task.objects.none()
    filterset_fields = ("subject",)

    def get_serializer_class(self, *args, **kwargs):
        if self.action == "list":
            return TaskListSerializer
        return TaskDetailSerializer

    def get_queryset(self):
        return Task.objects.filter(
            subject__study_group=self.request.user.study_group,
            deadline_at__gte=timezone.now(),
        )


class SubjectViewSet(ModelViewSet):
    """
    CRUD для учебных дисциплин.
    """

    queryset = Subject.objects.none()
    serializer_class = SubjectSerializer

    def get_queryset(self):
        return self.request.user.study_group.subjects.all()
