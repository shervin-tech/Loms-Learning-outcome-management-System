from curriculum.models import Curriculum
from django.shortcuts import render
from accounts.models import CustomUser
from accounts.decorators import role_required

@role_required(CustomUser.Role.LECTURER)
def lecturer_dashboard(request):
    """
    Lecturer kendi sorumlu olduğu Curriculum'ları görsün.
    """
    user = request.user
    curricula = (
        Curriculum.objects.filter(
            Q(lecturer=user) | Q(id__in=user.lecturer_curricula.values("id"))
        )
        .select_related("program")
        .distinct()
    )

    context = {
        "curricula": curricula,
    }
    return render(request, "curriculum/lecturer_dashboard.html", context)
