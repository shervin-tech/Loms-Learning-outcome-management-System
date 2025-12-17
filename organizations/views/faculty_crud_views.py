from django.shortcuts import render, redirect, get_object_or_404

from accounts.decorators import role_required
from accounts.models import CustomUser

from organizations.models import Program
from organizations.forms import ProgramForm


@role_required(CustomUser.Role.STUDENT_AFFAIRS)
def program_create(request):
    """
    Student Affairs için:
    - Yeni Program ekleme sayfası
    """
    if request.method == "POST":
        form = ProgramForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("organizations:faculty_program_list")
    else:
        form = ProgramForm()

    context = {"form": form}
    return render(request, "organizations/program_form.html", context)


@role_required(CustomUser.Role.STUDENT_AFFAIRS)
def program_edit(request, pk):
    program = get_object_or_404(Program, pk=pk)

    if request.method == "POST":
        form = ProgramForm(request.POST, instance=program)
        if form.is_valid():
            form.save()
            return redirect("organizations:faculty_program_list")
    else:
        form = ProgramForm(instance=program)

    context = {
        "form": form,
        "program": program,
    }
    return render(request, "organizations/program_form.html", context)


@role_required(CustomUser.Role.STUDENT_AFFAIRS)
def program_delete(request, pk):
    program = get_object_or_404(Program, pk=pk)

    if request.method == "POST":
        program.delete()
        return redirect("organizations:faculty_program_list")

    context = {
        "program": program,
    }
    return render(request, "organizations/program_confirm_delete.html", context)
