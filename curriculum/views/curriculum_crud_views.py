from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from accounts.decorators import role_required
from accounts.models import CustomUser

from curriculum.models import Curriculum
from curriculum.forms import CurriculumForm

from organizations.models import Program

@role_required(CustomUser.Role.STUDENT_AFFAIRS)
def curriculum_list(request):
    program_id = request.GET.get("program")
    if program_id:
        program = get_object_or_404(Program, id=program_id)
        curricula = Curriculum.objects.filter(program=program).select_related("program")
    else:
        program = None
        curricula = Curriculum.objects.select_related("program").all()

    context = {
        "curricula": curricula,
        "selected_program": program,
    }
    return render(request, "curriculum/curriculum_list.html", context)


@role_required(CustomUser.Role.STUDENT_AFFAIRS)
def curriculum_create(request):
    initial = {}
    program_id = request.GET.get("program")
    if program_id:
        initial["program"] = get_object_or_404(Program, id=program_id)

    if request.method == "POST":
        form = CurriculumForm(request.POST)
        if form.is_valid():
            curriculum = form.save()
            return redirect("curriculum:curriculum_list")
    else:
        form = CurriculumForm(initial=initial)

    context = {
        "form": form,
        "curriculum": None,  # edit ile aynı template'i kullanacağız
    }
    return render(request, "curriculum/curriculum_form.html", context)


@role_required(CustomUser.Role.STUDENT_AFFAIRS)
def curriculum_edit(request, pk):
    curriculum = get_object_or_404(Curriculum, pk=pk)

    if request.method == "POST":
        form = CurriculumForm(request.POST, instance=curriculum)
        if form.is_valid():
            form.save()  # save içinde zaten auto-enroll çalışıyor
            # Program filtresini korumak için query param ekleyelim
            return redirect(f"/curriculum/?program={curriculum.program.id}")
    else:
        form = CurriculumForm(instance=curriculum)

    context = {
        "form": form,
        "curriculum": curriculum,
    }
    return render(request, "curriculum/curriculum_form.html", context)

@role_required(CustomUser.Role.STUDENT_AFFAIRS)
def curriculum_delete(request, pk):
    curriculum = get_object_or_404(Curriculum, pk=pk)

    if request.method == "POST":
        program_id = curriculum.program.id
        curriculum.delete()
        return redirect(f"/curriculum/?program={program_id}")

    return render(
        request,
        "curriculum/curriculum_confirm_delete.html",
        {"curriculum": curriculum},
    )