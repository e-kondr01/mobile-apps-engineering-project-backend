from django.urls import path

from .views import StudyGroupCodeListView

urlpatterns = [path("study-groups/codes/", StudyGroupCodeListView.as_view())]
