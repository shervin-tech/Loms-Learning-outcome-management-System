from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from accounts.models import CustomUser

from accounts.decorators import role_required
from outcomes.models import ProgramOutcome
from organizations.models import Program
from outcomes.forms import ProgramOutcomeForm

from .permissions import _check_program_permission

@role_required(CustomUser.Role.FACULTY_MEMBER)
def program_outcome_manage(request, program_id):
    program = get_object_or_404(Program, id=program_id)
    _check_program_permission(request.user, program)

    outcomes = ProgramOutcome.objects.filter(program=program).order_by("order", "code")

    if request.method == "POST":
        form = ProgramOutcomeForm(request.POST)
        if form.is_valid():
            po = form.save(commit=False)
            po.program = program
            po.save()
            return redirect("outcomes:program_outcome_manage", program_id=program.id)
    else:
        form = ProgramOutcomeForm()

    context = {
        "program": program,
        "outcomes": outcomes,
        "form": form,
    }
    return render(request, "outcomes/program_outcome_manage.html", context)


@role_required(CustomUser.Role.FACULTY_MEMBER)
def program_outcome_edit(request, pk):
    po = get_object_or_404(ProgramOutcome, pk=pk)
    program = po.program
    _check_program_permission(request.user, program)

    if request.method == "POST":
        form = ProgramOutcomeForm(request.POST, instance=po)
        if form.is_valid():
            form.save()
            return redirect("outcomes:program_outcome_manage", program_id=program.id)
    else:
        form = ProgramOutcomeForm(instance=po)

    context = {
        "program": program,
        "form": form,
        "po": po,
    }
    return render(request, "outcomes/program_outcome_edit.html", context)


@role_required(CustomUser.Role.FACULTY_MEMBER)
def program_outcome_delete(request, pk):
    po = get_object_or_404(ProgramOutcome, pk=pk)
    program = po.program
    _check_program_permission(request.user, program)

    if request.method == "POST":
        po.delete()
        return redirect("outcomes:program_outcome_manage", program_id=program.id)

    context = {
        "program": program,
        "po": po,
    }
    return render(request, "outcomes/program_outcome_confirm_delete.html", context)

