from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return view.action in ('retrieve', 'list')

    def has_object_permission(self, request, view, obj):
        return obj == request.user
