from academic_plans.models import EducationalProgram, FieldOfStudy
from django.db.models import Q
from django_filters import rest_framework as filters


class FieldOfStudyFilter(filters.FilterSet):
    search = filters.CharFilter(
        method="search_filter",
        help_text="Поиск по коду и названию направления подготовки",
    )

    def search_filter(self, queryset, name, value):
        return queryset.filter(Q(title__icontains=value) | Q(number__icontains=value))

    class Meta:
        model = FieldOfStudy
        fields = ("search",)


class EducationalProgramFilter(filters.FilterSet):
    enrollment_year = filters.CharFilter(
        field_name="enrollment_year", lookup_expr="icontains"
    )
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")

    class Meta:
        model = EducationalProgram
        fields = ("title", "enrollment_year")
