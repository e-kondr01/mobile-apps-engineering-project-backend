import environ
from django_filters import rest_framework as filters
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView as TokenObtainPairViewNoExample,
)

from .models import StudyGroup
from .serializers import StudyGroupCodeSerializer

env = environ.Env()
test_user_email = env.str("DJANGO_TEST_USER_EMAIL", "email@example.com")
test_user_password = env.str("DJANGO_TEST_USER_PASSWORD", "password")


@extend_schema(
    examples=[
        OpenApiExample(
            "Тестовый пользователь",
            value={"email": test_user_email, "password": test_user_password},
            request_only=True,
        )
    ]
)
class TokenObtainPairView(TokenObtainPairViewNoExample):
    """
    Получение JWT для авторизации запросов.
    Для упрощения работы с локальным Swagger UI имеет пример реквизитов для входа.
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


# TODO: подтверждение почты
