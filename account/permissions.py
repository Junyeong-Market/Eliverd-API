from rest_framework.permissions import BasePermission

from account.user import AnonymousUser, NormalUser


class NotLoggedIn(BasePermission):
    def has_permission(self, request, view):
        return request.account is AnonymousUser


class LoggedIn(BasePermission):
    def has_permission(self, request, view):
        return request.account is NormalUser
