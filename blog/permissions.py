from rest_framework.permissions import BasePermission


class IsWriter(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.writer_profile


class IsEditor(BasePermission):
    def has_permission(self, request, view):
        return IsWriter().has_permission(request, view) and request.user.writer_profile.is_editor
