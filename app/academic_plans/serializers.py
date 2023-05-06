from academic_plans.models import EducationalProgram, FieldOfStudy
from rest_framework.serializers import ModelSerializer


class FieldOfStudySerializer(ModelSerializer):
    class Meta:
        model = FieldOfStudy
        fields = "__all__"


class EducationalProgramSerializer(ModelSerializer):
    class Meta:
        model = EducationalProgram
        fields = ("id", "title", "enrollment_year")
