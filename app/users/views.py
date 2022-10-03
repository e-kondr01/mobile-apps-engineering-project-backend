from django_filters import rest_framework as filters
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from .models import StudyGroup
from .serializers import StudyGroupCodeSerializer


class StudyGroupFilter(filters.FilterSet):
    q = filters.CharFilter(
        field_name="code", lookup_expr="istartswith", help_text="Поиск по коду группы"
    )

    class Meta:
        model = StudyGroup
        fields = ("q",)


class StudyGroupCodeListView(ListAPIView):
    """
    Список групп с их кодами
    """

    serializer_class = StudyGroupCodeSerializer
    queryset = StudyGroup.objects.filter(is_active=True)
    filterset_class = StudyGroupFilter
    permission_classes = (AllowAny,)
