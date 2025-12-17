from django.shortcuts import render, get_object_or_404, redirect

from accounts.decorators import role_required
from accounts.models import CustomUser

from organizations.forms import FacultyForm
from organizations.models import Faculty


@role_required(CustomUser.Role.STUDENT_AFFAIRS)
def faculty_edit(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)

    if request.method == "POST":
        form = FacultyForm(request.POST, instance=faculty)
        if form.is_valid():
            form.save()
            return redirect("organizations:faculty_program_list")
    else:
        form = FacultyForm(instance=faculty)

    context = {
        "faculty": faculty,
        "form": form,
    }
    return render(request, "organizations/faculty_form.html", context)

@role_required(CustomUser.Role.STUDENT_AFFAIRS)
def faculty_delete(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)

    if request.method == "POST":
        faculty.delete()
        return redirect("organizations:faculty_program_list")

    return render(request, "organizations/faculty_confirm_delete.html", {"faculty": faculty})
