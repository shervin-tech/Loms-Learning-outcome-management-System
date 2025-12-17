from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction

from accounts.decorators import role_required
from accounts.models import CustomUser

from outcomes.models import LearningOutcome, ProgramOutcome, LearningOutcomeProgramOutcome
# or whatever your mapping model is called

from .permissions import _check_program_permission  # if you use it

@role_required(CustomUser.Role.LECTURER)
def learning_outcome_mapping(request, pk):
    """
    Tek bir LO için:
    - Programdaki tüm PO'ları listeler
    - Her PO için yüzde girilerek mapping yapılır.
    """
    lo = get_object_or_404(
        LearningOutcome.objects.select_related("curriculum", "curriculum__program"),
        pk=pk,
    )
    curriculum = lo.curriculum
    _check_curriculum_permission_for_lecturer(request.user, curriculum)

    program = curriculum.program
    pos = ProgramOutcome.objects.filter(program=program).order_by("order", "code")

    # Mevcut mapping'leri dictionary olarak tutalım
    existing = {
        m.program_outcome_id: m
        for m in lo.lo_po_mappings.all()
    }

    if request.method == "POST":
        for po in pos:
            field_name = f"po_{po.id}"
            raw_value = request.POST.get(field_name, "").strip()

            # Boş → mapping sil
            if raw_value == "":
                mapping = existing.get(po.id)
                if mapping:
                    mapping.delete()
                continue

            # Sayıya çevir
            try:
                weight = int(raw_value)
            except ValueError:
                continue  # invalid input'u şimdilik ignore

            # 0 veya altı → mapping sil
            if weight <= 0:
                mapping = existing.get(po.id)
                if mapping:
                    mapping.delete()
                continue

            # 100'den büyükse clamp
            if weight > 100:
                weight = 100

            mapping = existing.get(po.id)
            if mapping:
                mapping.weight = weight
                mapping.save()
            else:
                LearningOutcomeProgramOutcome.objects.create(
                    learning_outcome=lo,
                    program_outcome=po,
                    weight=weight,
                )

        return redirect("outcomes:learning_outcome_manage", curriculum_id=curriculum.id)

    # GET → template'e PO + mevcut weight listesi gönder
    rows = []
    for po in pos:
        mapping = existing.get(po.id)
        rows.append(
            {
                "po": po,
                "weight": mapping.weight if mapping else "",
            }
        )

    context = {
        "curriculum": curriculum,
        "lo": lo,
        "rows": rows,
    }
    return render(request, "outcomes/learning_outcome_mapping.html", context)
