import environ
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView as TokenObtainPairViewNoExample,
)

from .models import StudyGroup, User
from .serializers import ActivationCodeSerializer, StudyGroupCodeSerializer

env = environ.Env()
test_access_token = env.str("TEST_ACCESS_TOKEN", "")
test_refresh_token = env.str("TEST_REFRESH_TOKEN", "")


@extend_schema(
    examples=[
        OpenApiExample(
            "Тестовый токен",
            value={"access": test_access_token, "refresh": test_refresh_token},
            response_only=True,
        )
    ]
)
class TokenObtainPairView(TokenObtainPairViewNoExample):
    """
    Получение JWT для авторизации запросов.
    """


class StudyGroupFilter(filters.FilterSet):
    q = filters.CharFilter(
        field_name="code", lookup_expr="icontains", help_text="Поиск по коду группы"
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


class UserActivationView(APIView):
    """
    Активация аккаунта пользователя
    """

    serializer_class = ActivationCodeSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(User, email=serializer.validated_data["email"])
        code_in_cache = cache.get(f"tasks_backend:activation_codes:{user.pk}")

        if serializer.validated_data["code"] == code_in_cache:
            user.is_active = True
            user.save()

            return Response({"result": "Успешная активация"})

        return Response({"error": "Неверный код"}, status=status.HTTP_400_BAD_REQUEST)
