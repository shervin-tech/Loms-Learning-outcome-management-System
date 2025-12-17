from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from accounts.decorators import role_required
from accounts.models import CustomUser
from curriculum.models import Curriculum
from assessments.models import Assessment

from .permissions import _check_curriculum_permission_for_lecturer

@role_required(CustomUser.Role.LECTURER)
def assessment_manage(request, curriculum_id):
    """
    Belirli bir curriculum için assessment listesi + yeni assessment ekleme formu.
    """
    curriculum = get_object_or_404(
        Curriculum.objects.select_related("program"),
        id=curriculum_id,
    )
    _check_curriculum_permission_for_lecturer(request.user, curriculum)

    assessments = curriculum.assessments.all().order_by("date", "name")

    AssessmentForm = modelform_factory(
        Assessment,
        fields=[ "type", "weight_in_course", "max_score", "date"],
    )

    if request.method == "POST":
        form = AssessmentForm(request.POST)
        if form.is_valid():
            assessment = form.save(commit=False)
            assessment.curriculum = curriculum
            assessment.save()
            return redirect("assessments:assessment_manage", curriculum_id=curriculum.id)
    else:
        form = AssessmentForm()

    context = {
        "curriculum": curriculum,
        "assessments": assessments,
        "form": form,
    }
    return render(request, "assessments/assessment_manage.html", context)

@role_required(CustomUser.Role.LECTURER)
def assessment_edit(request, pk):
    assessment = get_object_or_404(
        Assessment.objects.select_related("curriculum", "curriculum__program"),
        pk=pk,
    )
    curriculum = assessment.curriculum
    _check_curriculum_permission_for_lecturer(request.user, curriculum)

    AssessmentForm = modelform_factory(
        Assessment,
        fields=[ "type", "weight_in_course", "max_score", "date"],
    )

    if request.method == "POST":
        form = AssessmentForm(request.POST, instance=assessment)
        if form.is_valid():
            form.save()
            return redirect("assessments:assessment_manage", curriculum_id=curriculum.id)
    else:
        form = AssessmentForm(instance=assessment)

    context = {
        "curriculum": curriculum,
        "assessment": assessment,
        "form": form,
    }
    return render(request, "assessments/assessment_edit.html", context)

@role_required(CustomUser.Role.LECTURER)
def assessment_delete(request, pk):
    assessment = get_object_or_404(
        Assessment.objects.select_related("curriculum", "curriculum__program"),
        pk=pk,
    )
    curriculum = assessment.curriculum
    _check_curriculum_permission_for_lecturer(request.user, curriculum)

    if request.method == "POST":
        assessment.delete()
        return redirect("assessments:assessment_manage", curriculum_id=curriculum.id)

    context = {
        "curriculum": curriculum,
        "assessment": assessment,
    }
    return render(request, "assessments/assessment_confirm_delete.html", context)
