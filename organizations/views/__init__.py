from .program_crud_views import faculty_program_list
from .faculty_crud_views import program_create, program_edit, program_delete
from .faculty_program_list_view import faculty_edit, faculty_delete
from .faculty_dashboard_views import faculty_member_dashboard

__all__ = [
    "faculty_program_list",
    "program_create",
    "program_edit",
    "program_delete",
    "faculty_edit",
    "faculty_delete",
    "faculty_member_dashboard",
]
