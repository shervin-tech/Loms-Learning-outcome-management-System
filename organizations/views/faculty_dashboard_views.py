from django.shortcuts import render

from accounts.decorators import role_required
from accounts.models import CustomUser

from organizations.models import Faculty, Program

@role_required(CustomUser.Role.FACULTY_MEMBER)
def faculty_member_dashboard(request):
    user = request.user

    if user.is_admin:
        faculties = Faculty.objects.all()
    else:
        faculties = Faculty.objects.filter(responsible=user)

    programs = Program.objects.filter(faculty__in=faculties).select_related("faculty")

    context = {
        "faculties": faculties,
        "programs": programs,
    }
    return render(request, "organizations/faculty_member_dashboard.html", context)
