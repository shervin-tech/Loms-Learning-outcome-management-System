from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction

from accounts.decorators import role_required
from accounts.models import CustomUser
from assessments.models import Assessment, AssessmentLearningOutcome
from outcomes.models import LearningOutcome

from .permissions import _check_curriculum_permission_for_lecturer

@role_required(CustomUser.Role.LECTURER)
def assessment_lo_mapping(request, pk):
    """
    Tek bir assessment için:
    - Curriculum'daki tüm LO'ları listeler
    - Her LO için yüzde girilerek mapping yapılır.
    """
    assessment = get_object_or_404(
        Assessment.objects.select_related("curriculum", "curriculum__program"),
        pk=pk,
    )
    curriculum = assessment.curriculum
    _check_curriculum_permission_for_lecturer(request.user, curriculum)

    los = LearningOutcome.objects.filter(
        curriculum=curriculum
    ).order_by("code")

    existing = {
        m.learning_outcome_id: m
        for m in assessment.lo_mappings.all()
    }

    if request.method == "POST":
        for lo in los:
            field_name = f"lo_{lo.id}"
            raw_value = request.POST.get(field_name, "").strip()

            # Boş ise → mapping sil
            if raw_value == "":
                mapping = existing.get(lo.id)
                if mapping:
                    mapping.delete()
                continue

            try:
                weight = int(raw_value)
            except ValueError:
                continue  # invalid input'u ignore

            if weight <= 0:
                mapping = existing.get(lo.id)
                if mapping:
                    mapping.delete()
                continue

            if weight > 100:
                weight = 100

            mapping = existing.get(lo.id)
            if mapping:
                mapping.weight_in_assessment = weight
                mapping.save()
            else:
                AssessmentLearningOutcome.objects.create(
                    assessment=assessment,
                    learning_outcome=lo,
                    weight_in_assessment=weight,
                )

        return redirect("assessments:assessment_manage", curriculum_id=curriculum.id)

    # GET: template için satır listesi
    rows = []
    for lo in los:
        mapping = existing.get(lo.id)
        rows.append(
            {
                "lo": lo,
                "weight": mapping.weight_in_assessment if mapping else "",
            }
        )

    context = {
        "curriculum": curriculum,
        "assessment": assessment,
        "rows": rows,
    }
    return render(request, "assessments/assessment_lo_mapping.html", context)

