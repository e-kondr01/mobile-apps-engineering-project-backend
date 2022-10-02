from django.utils import timezone
from rest_framework.viewsets import ModelViewSet

from .models import Task
from .serializers import TaskListSerializer


class TaskViewSet(ModelViewSet):
    serializer_class = TaskListSerializer
    queryset = Task.objects.none()

    def get_queryset(self):
        return Task.objects.filter(
            subject__study_group=self.request.user.study_group,
            deadline_at__gte=timezone.now(),
        )
