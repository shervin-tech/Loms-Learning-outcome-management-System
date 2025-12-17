from django.core.exceptions import PermissionDenied
from accounts.models import CustomUser
from curriculum.models import Curriculum

def _check_curriculum_permission_for_lecturer(user: CustomUser, curriculum: Curriculum):
    """
    Lecturer sadece kendisine atanmış curriculum'lar için assessment yönetebilsin.
    Admin her şeye girebilir.
    """
    if user.is_admin:
        return

    # Ana lecturer FK kontrolü
    if getattr(curriculum, "lecturer_id", None) == user.id:
        return

    # Eğer M2M 'lecturers' alanı varsa, onu da kontrol et
    if hasattr(curriculum, "lecturers") and curriculum.lecturers.filter(id=user.id).exists():
        return

    raise PermissionDenied("You are not allowed to manage assessments for this curriculum.")
