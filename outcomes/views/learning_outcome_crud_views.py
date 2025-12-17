from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from accounts.decorators import role_required
from accounts.models import CustomUser

from curriculum.models import Curriculum
from outcomes.models import LearningOutcome
from outcomes.forms import LearningOutcomeForm

from .permissions import _check_curriculum_permission_for_lecturer

@role_required(CustomUser.Role.LECTURER)
def learning_outcome_manage(request, curriculum_id):
    curriculum = get_object_or_404(
        Curriculum.objects.select_related("program"),
        id=curriculum_id,
    )
    _check_curriculum_permission_for_lecturer(request.user, curriculum)

    los = LearningOutcome.objects.filter(
        curriculum=curriculum
    ).prefetch_related("program_outcomes")

    if request.method == "POST":
        form = LearningOutcomeForm(request.POST)
        if form.is_valid():
            lo = form.save(commit=False)
            lo.curriculum = curriculum
            lo.save()
            return redirect("outcomes:learning_outcome_manage", curriculum_id=curriculum.id)
    else:
        form = LearningOutcomeForm()

    context = {
        "curriculum": curriculum,
        "los": los,
        "form": form,
    }
    return render(request, "outcomes/learning_outcome_manage.html", context)


@role_required(CustomUser.Role.LECTURER)
def learning_outcome_edit(request, pk):
    lo = get_object_or_404(
        LearningOutcome.objects.select_related("curriculum", "curriculum__program"),
        pk=pk,
    )
    curriculum = lo.curriculum
    _check_curriculum_permission_for_lecturer(request.user, curriculum)

    if request.method == "POST":
        form = LearningOutcomeForm(request.POST, instance=lo)
        if form.is_valid():
            form.save()
            return redirect("outcomes:learning_outcome_manage", curriculum_id=curriculum.id)
    else:
        form = LearningOutcomeForm(instance=lo)

    context = {
        "curriculum": curriculum,
        "form": form,
        "lo": lo,
    }
    return render(request, "outcomes/learning_outcome_edit.html", context)

@role_required(CustomUser.Role.LECTURER)
def learning_outcome_delete(request, pk):
    lo = get_object_or_404(
        LearningOutcome.objects.select_related("curriculum", "curriculum__program"),
        pk=pk,
    )
    curriculum = lo.curriculum
    _check_curriculum_permission_for_lecturer(request.user, curriculum)

    if request.method == "POST":
        lo.delete()
        return redirect("outcomes:learning_outcome_manage", curriculum_id=curriculum.id)

    context = {
        "curriculum": curriculum,
        "lo": lo,
    }
    return render(request, "outcomes/learning_outcome_confirm_delete.html", context)
