from django.core.exceptions import PermissionDenied

from accounts.models import CustomUser
from organizations.models import Program
from curriculum.models import Curriculum


def _check_program_permission(user: CustomUser, program: Program):
    """
    Faculty Member sadece sorumlu olduğu faculty'deki programlar için
    PO düzenleyebilsin. Admin her yere girebilir.
    """
    if user.is_admin:
        return
    if program.faculty.responsible_id != user.id:
        raise PermissionDenied("You are not allowed to manage this program.")

def _check_curriculum_permission_for_lecturer(user: CustomUser, curriculum: Curriculum):
    """
    Lecturer sadece kendisine atanmış curriculum'lar için LO yönetebilsin.
    Admin her şeye girebilir.
    """
    if user.is_admin:
        return
    if curriculum.lecturer_id != user.id:
        raise PermissionDenied("You are not allowed to manage this curriculum.")
