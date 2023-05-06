from academic_plans.serializers import (
    EducationalProgramSerializer,
    FieldOfStudySerializer,
)
from django.conf import settings
from djoser.serializers import UserSerializer
from rest_framework import serializers


class CurrentUserSerializer(UserSerializer):
    field_of_study = FieldOfStudySerializer(read_only=True)
    educational_program = EducationalProgramSerializer(read_only=True)


class ActivationCodeSerializer(serializers.Serializer):
    code = serializers.CharField()
    email = serializers.EmailField()

    def validate_code(self, code: str) -> str:
        if len(code) != settings.ACTIVATION_CODE_LENGTH:
            raise serializers.ValidationError(
                f"Код должен иметь длину {settings.ACTIVATION_CODE_LENGTH} символа"
            )
        if not code.isdigit():
            raise serializers.ValidationError("Код должен состоять только из цифр")
        return code
