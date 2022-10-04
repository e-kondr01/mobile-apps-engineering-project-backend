from djoser.serializers import UserSerializer
from rest_framework import serializers

from .models import StudyGroup


class StudyGroupCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyGroup
        fields = ("id", "code")


class StudyGroupSerializer(serializers.ModelSerializer):
    education_level = serializers.CharField(source="get_education_level_display")

    class Meta:
        model = StudyGroup
        fields = ("id", "code", "program_name", "enrollment_year", "education_level")


class CurrentUserSerializer(UserSerializer):
    study_group = StudyGroupCodeSerializer(read_only=True)
