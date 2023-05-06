from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .examples import TASK_DATE_GROUPS_RESPONSE_EXAMPLE
from .models import Subject, SubjectInAcademicPlan, Task
from .serializers import (
    PutTaskSerializer,
    SubjectListSerializer,
    SubjectSerializer,
    TaskDateGroupSerializer,
    TaskDetailSerializer,
    TaskListSerializer,
    UpdateSubjectSerializer,
)


class TaskFilter(filters.FilterSet):
    title = filters.CharFilter(
        field_name="title",
        lookup_expr="icontains",
        help_text="Поиск по названию задания",
    )

    status = filters.CharFilter(method="filter_by_status")

    subject = filters.NumberFilter(field_name="subject_entry")

    def filter_by_status(self, queryset: QuerySet, name, value: str) -> QuerySet:
        if value == Task.Status.COMPLETED.value:
            # Только те, которые завершены пользователем
            queryset = queryset.filter(completed_by=self.request.user)

        elif value == Task.Status.TODO.value:
            # Исключаем те, которые были завершены
            queryset = queryset.exclude(completed_by=self.request.user)
            # Аннотируем просроченные
            queryset = Task.annotate_overdue(queryset)
            # Аннотируем срочные
            queryset = Task.annotate_urgent(queryset)

        return queryset

    class Meta:
        model = Task
        fields = ("title", "subject")


schema_status_parameter = extend_schema(
    parameters=[
        OpenApiParameter(
            "status",
            str,
            OpenApiParameter.QUERY,
            description='Фильтр "Актуальное/Выполненное"',
            enum=["todo", "completed"],
            default="todo",
        )
    ]
)


@extend_schema_view(list=schema_status_parameter, date_groups=schema_status_parameter)
class TaskViewSet(ModelViewSet):
    """
    CRUD для задач.
    """

    queryset = Task.objects.none()
    filterset_class = TaskFilter

    def get_serializer_class(self):
        if self.action == "list":
            return TaskListSerializer
        if self.action == "date_groups":
            return TaskDateGroupSerializer
        if self.action == "retrieve":
            return TaskDetailSerializer
        return PutTaskSerializer

    def filter_queryset(self, queryset):
        queryset: QuerySet = super().filter_queryset(queryset)
        queryset = queryset.select_related("subject_entry__subject")
        return queryset

    def get_queryset(self):
        subject_entry_ids = (
            self.request.user.educational_program.academic_plan.subject_entries.filter(
                semesters__contains=[
                    self.request.user.educational_program.current_semester
                ]
            ).values_list("id", flat=True)
        )
        return Task.objects.filter(subject_entry_id__in=subject_entry_ids)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @extend_schema(
        examples=[
            OpenApiExample("Example", value=TASK_DATE_GROUPS_RESPONSE_EXAMPLE),
        ],
    )
    @action(detail=False, methods=["get"])
    def date_groups(self, request):
        """
        Список задач, сгруппированный по датам.
        """
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)

        resp = {"No deadline": []}
        serialized_task: dict

        for serialized_task in serializer.data:
            deadline_at_str = serialized_task["deadline_at"]
            # Задача с дедлайном
            if deadline_at_str:
                # Получаем строку даты
                date_str = deadline_at_str.split("T")[0]
                if date_str in resp:
                    resp[date_str].append(serialized_task)
                else:
                    resp[date_str] = [serialized_task]
            else:
                # Задача без дедлайна
                resp["No deadline"].append(serialized_task)
        return Response(resp)


class SubjectFilter(filters.FilterSet):
    title = filters.CharFilter(
        field_name="subject__title",
        lookup_expr="icontains",
        help_text="Поиск названию предмета",
    )

    class Meta:
        model = SubjectInAcademicPlan
        fields = ("title",)


class SubjectViewSet(UpdateModelMixin, ReadOnlyModelViewSet):
    """
    CRUD для учебных дисциплин.
    """

    queryset = SubjectInAcademicPlan.objects.none()
    filterset_class = SubjectFilter

    def get_serializer_class(self):
        if self.action == "list":
            return SubjectListSerializer
        if self.action == "retrieve":
            return SubjectSerializer
        return UpdateSubjectSerializer

    def get_queryset(self):
        return (
            self.request.user.educational_program.academic_plan.subject_entries.filter(
                semesters__contains=[
                    self.request.user.educational_program.current_semester
                ]
            )
        )


class CompleteTaskView(APIView):
    def put(self, request, *args, **kwargs):
        """
        Пометить задание как выполненное
        """
        task: Task = get_object_or_404(Task, pk=self.kwargs["pk"])
        task.completed_by.add(request.user)

        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        """
        Пометить задание как невыполненное
        """
        task: Task = get_object_or_404(Task, pk=self.kwargs["pk"])
        task.completed_by.remove(request.user)

        return Response(status=status.HTTP_204_NO_CONTENT)
