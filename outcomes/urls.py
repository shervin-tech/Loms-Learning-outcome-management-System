from django.urls import path

from .views.program_outcome_crud_views import (
    program_outcome_manage, program_outcome_edit, program_outcome_delete
)
from .views.learning_outcome_crud_views import (
    learning_outcome_manage, learning_outcome_edit, learning_outcome_delete
)
from .views.learning_outcome_mapping_views import learning_outcome_mapping

app_name = "outcomes"

urlpatterns = [
    # Program outcomes
    path("program/<int:program_id>/outcomes/", program_outcome_manage, name="program_outcome_manage"),
    path("program-outcome/<int:pk>/edit/", program_outcome_edit, name="program_outcome_edit"),
    path("program-outcome/<int:pk>/delete/", program_outcome_delete, name="program_outcome_delete"),

    # Learning outcomes
    path("curriculum/<int:curriculum_id>/learning-outcomes/", learning_outcome_manage, name="learning_outcome_manage"),
    path("learning-outcome/<int:pk>/edit/", learning_outcome_edit, name="learning_outcome_edit"),
    path("learning-outcome/<int:pk>/delete/", learning_outcome_delete, name="learning_outcome_delete"),

    # LO ↔ PO mapping
    path("learning-outcome/<int:pk>/mapping/", learning_outcome_mapping, name="learning_outcome_mapping"),
]
