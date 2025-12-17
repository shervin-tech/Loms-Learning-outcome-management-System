from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from accounts.decorators import role_required
from accounts.models import CustomUser

from organizations.models import Faculty
from organizations.forms import FacultyForm

@role_required(CustomUser.Role.STUDENT_AFFAIRS)
def faculty_program_list(request):
    """
    Student Affairs için:
    - Tüm Faculty + Program'ları listeler
    - Yeni Faculty ekleme formu gösterir
    """
    faculties = Faculty.objects.prefetch_related("programs").all()
    faculty_form = FacultyForm()

    if request.method == "POST":
        faculty_form = FacultyForm(request.POST)
        if faculty_form.is_valid():
            faculty_form.save()
            return redirect("organizations:faculty_program_list")

    context = {
        "faculties": faculties,
        "faculty_form": faculty_form,
    }
    return render(request, "organizations/faculty_program_list.html", context)
