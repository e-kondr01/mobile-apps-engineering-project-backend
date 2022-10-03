from django.db.models import QuerySet
from django.utils import timezone
from django_filters import rest_framework as filters
from rest_framework.viewsets import ModelViewSet

from .models import Subject, Task
from .serializers import SubjectSerializer, TaskDetailSerializer, TaskListSerializer


class TaskFilter(filters.FilterSet):
    title = filters.CharFilter(
        field_name="title",
        lookup_expr="icontains",
        help_text="Поиск по названию задания",
    )

    class Meta:
        model = Task
        fields = ("title", "subject")


class TaskViewSet(ModelViewSet):
    """
    CRUD для задач.
    """

    queryset = Task.objects.none()
    filterset_class = TaskFilter

    def get_serializer_class(self, *args, **kwargs):
        if self.action == "list":
            return TaskListSerializer
        return TaskDetailSerializer

    def filter_queryset(self, queryset):
        queryset: QuerySet = super().filter_queryset(queryset)
        queryset = queryset.select_related("subject")
        return queryset

    def get_queryset(self):
        return Task.objects.filter(
            subject__study_group=self.request.user.study_group,
            deadline_at__gte=timezone.now(),
        )


class SubjectFilter(filters.FilterSet):
    title = filters.CharFilter(
        field_name="title",
        lookup_expr="icontains",
        help_text="Поиск названию предмета",
    )

    class Meta:
        model = Subject
        fields = ("title",)


class SubjectViewSet(ModelViewSet):
    """
    CRUD для учебных дисциплин.
    """

    queryset = Subject.objects.none()
    serializer_class = SubjectSerializer
    filterset_class = SubjectFilter

    def get_queryset(self):
        return self.request.user.study_group.subjects.all()
