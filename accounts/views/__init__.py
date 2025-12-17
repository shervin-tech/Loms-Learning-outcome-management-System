from .user_management_views import user_create, user_edit, user_delete
from .role_redirect_views import role_redirect
from .Student_dashboard_views import student_dashboard, student_course_detail

__all__ = [
    "user_create",
    "user_edit",
    "user_delete",
    "role_redirect",
    "student_dashboard",
    "student_course_detail",
]
