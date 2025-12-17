from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse

from accounts.models import CustomUser


@login_required
def role_redirect(request):
    user: CustomUser = request.user

    # 1) Admin  Django admin
    if user.is_admin or user.is_superuser:
        return redirect(reverse("admin:index"))

    # 2) Student Affairs  Org Panel (faklte / program y”netimi)
    if user.is_student_affairs:
        return redirect("organizations:faculty_program_list")

    # 3) Faculty Member  Faculty Panel
    if user.is_faculty_member:
        return redirect("organizations:faculty_member_dashboard")

    # 4) Lecturer  Lecturer Dashboard
    if user.is_lecturer:
        return redirect("curriculum:lecturer_dashboard")

    # 5) Student  simdilik Org Panel veya ileride Student Dashboard
    if user.is_student:
        return redirect("accounts:student_dashboard")
    
    # Fallback: login sayfasÕna veya ana sayfaya d”n
    return redirect("accounts:login")
