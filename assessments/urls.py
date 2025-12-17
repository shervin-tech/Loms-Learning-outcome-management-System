from django.urls import path

from .views.assessment_crud_views import assessment_manage, assessment_edit, assessment_delete
from .views.assessment_lo_mapping_views import assessment_lo_mapping
from .views.assessment_grading_views import assessment_grade_manage

app_name = "assessments"

urlpatterns = [
    path("curriculum/<int:curriculum_id>/", assessment_manage, name="assessment_manage"),
    path("assessment/<int:pk>/edit/", assessment_edit, name="assessment_edit"),
    path("assessment/<int:pk>/delete/", assessment_delete, name="assessment_delete"),
    path("assessment/<int:pk>/lo-mapping/", assessment_lo_mapping, name="assessment_lo_mapping"),
    path("<int:pk>/grades/", assessment_grade_manage, name="assessment_grade_manage"),
]


# app_name = "assessments"

# urlpatterns = [
#     path(
#         "curriculum/<int:curriculum_id>/",
#         views.assessment_manage,
#         name="assessment_manage",
#     ),
#     path(
#         "assessment/<int:pk>/edit/",
#         views.assessment_edit,
#         name="assessment_edit",
#     ),
#     path(
#         "assessment/<int:pk>/delete/",
#         views.assessment_delete,
#         name="assessment_delete",
#     ),
#     path(
#         "assessment/<int:pk>/lo-mapping/",
#         views.assessment_lo_mapping,
#         name="assessment_lo_mapping",
#     ),
# 	path(
# 		"<int:pk>/grades/",
# 		views.assessment_grade_manage,
# 		name="assessment_grade_manage",
# 	),

# ]
