from rest_framework.permissions import BasePermission


class NotLoggedIn(BasePermission):
    def has_permission(self, request, view):
        return not request.user


class LoggedIn(BasePermission):
    def has_permission(self, request, view):
        return request.user
