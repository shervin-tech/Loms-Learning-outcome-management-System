from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required
from accounts.forms import UserCreateForm
from accounts.models import CustomUser


@role_required(CustomUser.Role.STUDENT_AFFAIRS)
def user_create(request):
    """
    Student Affairs:
    - Student
    - Lecturer
    - Faculty Member
    hesaplarını buradan oluşturabilsin.
    """
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("accounts:user_create")  # tekrar boş form
    else:
        form = UserCreateForm()

    users = (
        CustomUser.objects
        .order_by("username")
        .select_related(
            "student_faculty",
            "student_program",
            "faculty_member_faculty",
        )
    )

    context = {
        "form": form,
        "users": users,
    }
    return render(request, "accounts/user_create.html", context)


@role_required(CustomUser.Role.STUDENT_AFFAIRS)
def user_edit(request, pk):
    """
    Student Affairs mevcut kullanıcıların temel bilgilerini güncelleyebilsin.
    """
    user_obj = get_object_or_404(CustomUser, pk=pk)

    if user_obj.is_superuser:
        raise PermissionDenied("You cannot edit superuser accounts.")

    if request.method == "POST":
        form = UserCreateForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            return redirect("accounts:user_create")
    else:
        form = UserCreateForm(instance=user_obj)

    context = {
        "form": form,
        "edited_user": user_obj,
    }
    return render(request, "accounts/user_edit.html", context)


@role_required(CustomUser.Role.STUDENT_AFFAIRS)
def user_delete(request, pk):
    """
    Student Affairs kullanıcıları silebilsin.
    """
    user_obj = get_object_or_404(CustomUser, pk=pk)

    if user_obj.is_superuser:
        raise PermissionDenied("You cannot delete superuser accounts.")

    if request.method == "POST":
        user_obj.delete()
        return redirect("accounts:user_create")

    context = {
        "user_obj": user_obj,
    }
    return render(request, "accounts/user_confirm_delete.html", context)
