from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
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


class UserCreateSerializer(DjoserUserCreateSerializer):
    class Meta(DjoserUserCreateSerializer.Meta):
        fields = DjoserUserCreateSerializer.Meta.fields + ("study_group",)
