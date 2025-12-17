from django.urls import path
from .views.curriculum_crud_views import (
    curriculum_list, curriculum_create, curriculum_edit, curriculum_delete
)

app_name = "curriculum"

urlpatterns = [
    path("", curriculum_list, name="curriculum_list"),
    path("create/", curriculum_create, name="curriculum_create"),
    path("<int:pk>/edit/", curriculum_edit, name="curriculum_edit"),
    path("<int:pk>/delete/", curriculum_delete, name="curriculum_delete"),
]
