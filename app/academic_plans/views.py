from academic_plans.filters import EducationalProgramFilter, FieldOfStudyFilter
from academic_plans.models import EducationalProgram, FieldOfStudy
from academic_plans.serializers import (
    EducationalProgramSerializer,
    FieldOfStudySerializer,
)
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny


class FieldOfStudyListView(ListAPIView):
    """
    Список направлений подготовки.
    """

    queryset = FieldOfStudy.objects.all()
    serializer_class = FieldOfStudySerializer
    filterset_class = FieldOfStudyFilter
    permission_classes = (AllowAny,)


class EducationalProgramListView(ListAPIView):
    """
    Список образовательных программ.
    """

    queryset = EducationalProgram.objects.all()
    serializer_class = EducationalProgramSerializer
    filterset_class = EducationalProgramFilter
    permission_classes = (AllowAny,)
