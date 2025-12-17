from django.shortcuts import render, get_object_or_404

from accounts.decorators import role_required
from accounts.models import CustomUser
from assessments.models import Assessment, StudentAssessmentResult
from curriculum.models import Curriculum


@role_required(CustomUser.Role.STUDENT)
def student_dashboard(request):
    user: CustomUser = request.user

    # Öğrencinin programı ve sınıfı (grade)
    student_program = user.student_program      
    student_grade = user.student_grade          

    curricula = Curriculum.objects.none()
    if student_program and student_grade:
        curricula = (
            Curriculum.objects
            .filter(
                program=student_program,        
                year=student_grade,             
            )
            .order_by("semester", "code")
        )

    context = {
        "student": user,
        "program": student_program,
        "grade": student_grade,
        "curricula": curricula,
    }
    return render(request, "accounts/student_dashboard.html", context)

@role_required(CustomUser.Role.STUDENT)
def student_course_detail(request, curriculum_id):
    """
    Öğrenci için tek bir dersin:
    - temel bilgileri
    - assessment listesi + kendi notu
    - assessment → LO → PO mapping
    gösterilir.
    """
    user: CustomUser = request.user

    student_program = getattr(user, "student_program", None)
    student_grade = getattr(user, "student_grade", None)

    # Öğrencinin program + grade'ine ait olmayan derse girmesin
    curriculum = get_object_or_404(
        Curriculum.objects.select_related("program", "lecturer"),
        id=curriculum_id,
        program=student_program,
        year=student_grade,
    )

    # İlgili dersin tüm assessment'ları
    assessments = (
        Assessment.objects.filter(curriculum=curriculum)
        .prefetch_related(
            "lo_mappings__learning_outcome__lo_po_mappings__program_outcome",
            "results",
        )
        .order_by("date", "name")
    )

    # Bu öğrenciye ait notlar
    results_by_assessment = {
        r.assessment_id: r
        for r in StudentAssessmentResult.objects.filter(
            assessment__curriculum=curriculum,
            student=user,
        )
    }

    rows = []
    for a in assessments:
        result = results_by_assessment.get(a.id)

        # yaklaşık katkı hesabı (score / max_score * weight_in_course)
        contribution = None
        if (
            result is not None
            and result.raw_score is not None
            and a.max_score
        ):
            try:
                contribution = (result.raw_score / a.max_score) * a.weight_in_course
            except ZeroDivisionError:
                contribution = None

        # Assessment → LO → PO yapısı
        lo_rows = []
        for mapping in a.lo_mappings.all():
            lo = mapping.learning_outcome

            po_rows = []
            for lo_po in lo.lo_po_mappings.all():
                po_rows.append(
                    {
                        "po": lo_po.program_outcome,
                        "weight": lo_po.weight,
                    }
                )

            lo_rows.append(
                {
                    "lo": lo,
                    "weight_in_assessment": mapping.weight_in_assessment,
                    "po_rows": po_rows,
                }
            )

        score_value = None
        if result is not None:
            score_value = getattr(result, "raw_score", None)
            if score_value is None:
                score_value = getattr(result, "score", None)

        rows.append(
            {
                "assessment": a,
                "result": result,
                "contribution": contribution,
                "lo_rows": lo_rows,
                "score_value": score_value,
            }
        )

    context = {
        "student": user,
        "curriculum": curriculum,
        "rows": rows,
    }
    return render(request, "accounts/student_course_detail.html", context)
