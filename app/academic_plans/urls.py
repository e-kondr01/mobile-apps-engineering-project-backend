from academic_plans import views
from django.urls import path

urlpatterns = [
    path(
        "fields-of-study/",
        views.FieldOfStudyListView.as_view(),
    ),
    path(
        "educational-programs/",
        views.EducationalProgramListView.as_view(),
    ),
]
