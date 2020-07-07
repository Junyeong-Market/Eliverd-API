import logging

from rest_framework.permissions import BasePermission

from account.user import AnonymousUser, NormalUser

logger = logging.getLogger(__name__)


class NotLoggedIn(BasePermission):
    def has_permission(self, request, view):
        return request.account is AnonymousUser


class LoggedIn(BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.account, NormalUser)
