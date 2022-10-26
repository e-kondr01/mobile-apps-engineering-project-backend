from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from users.views import TokenObtainPairView, UserActivationView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/auth/users/activation/", UserActivationView.as_view()),
    path("api/auth/", include("djoser.urls")),
    path("api/auth/jwt/create/", TokenObtainPairView.as_view(), name="jwt-create"),
    path("api/auth/", include("djoser.urls.jwt")),
    path("api/", include("tasks.urls")),
    path("api/users/", include("users.urls")),
]
