import logging
from datetime import datetime

from account.models import Session
from account.user import AnonymousUser, NormalUser

logger = logging.getLogger(__name__)


class AuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            session = Session.objects.get(id=request.headers.get('Authorization', -1), expireAt__gte=datetime.now())
            request.account = NormalUser(session.pid)
        except Session.DoesNotExist:

            request.account = AnonymousUser

        response = self.get_response(request)

        return response
