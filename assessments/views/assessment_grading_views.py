from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction

from accounts.decorators import role_required
from accounts.models import CustomUser
from assessments.models import Assessment, StudentAssessmentResult
from .permissions import _check_curriculum_permission_for_lecturer

@role_required(CustomUser.Role.LECTURER)
def assessment_grade_manage(request, pk):
    """
    Tek bir assessment için öğrencilerin notlarını girme / güncelleme ekranı.
    Burada **raw_score** alanını kullanıyoruz; `score` field'ı yok.
    """
    assessment = get_object_or_404(
        Assessment.objects.select_related("curriculum", "curriculum__program"),
        pk=pk,
    )
    curriculum = assessment.curriculum
    _check_curriculum_permission_for_lecturer(request.user, curriculum)

    # Bu dersin öğrencileri
    students = curriculum.students.all().order_by("last_name", "first_name", "username")

    # Mevcut sonuçları çek
    existing_results = StudentAssessmentResult.objects.filter(
        assessment=assessment,
        student__in=students,
    )
    results_by_student = {r.student_id: r for r in existing_results}

    if request.method == "POST":
        for student in students:
            field_name = f"student_{student.id}"
            raw_value = request.POST.get(field_name, "").strip()

            # Boş bırakıldıysa → kaydı sil veya dokunma
            if raw_value == "":
                # İstersen burada var olan kaydı silebilirsin:
                # existing = results_by_student.get(student.id)
                # if existing:
                #     existing.delete()
                continue

            try:
                score_val = Decimal(raw_value)
            except (InvalidOperation, ValueError):
                # Geçersiz giriş → ignore
                continue

            # update_or_create: aynı öğrenci+assessment için tek kayıt
            StudentAssessmentResult.objects.update_or_create(
                student=student,
                assessment=assessment,
                defaults={
                    "raw_score": score_val,      # 🟩 asıl not
                },
            )

        return redirect("assessments:assessment_grade_manage", pk=assessment.id)

    # GET: tablo için satırları hazırla
    rows = []
    for student in students:
        result = results_by_student.get(student.id)

        score_value = None
        if result is not None:
            # Hem eski hem yeni world ile uyumlu kalmak için:
            score_value = getattr(result, "score", None)
            if score_value is None:
                score_value = getattr(result, "raw_score", None)

        rows.append(
            {
                "student": student,
                "result": result,
                "score": score_value,
            }
        )

    context = {
        "curriculum": curriculum,
        "assessment": assessment,
        "rows": rows,
    }
    return render(request, "assessments/assessment_grade_manage.html", context)
