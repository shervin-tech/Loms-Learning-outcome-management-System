from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'ADMIN'

class IsFaculty(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'FACULTY'

class IsLecturer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'LECTURER'

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'STUDENT'
