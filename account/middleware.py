import logging
from datetime import datetime

from django.utils.deprecation import MiddlewareMixin

from account.models import Session
from account.user import AnonymousUser, NormalUser

logger = logging.getLogger(__name__)


class AuthorizationMiddleware(MiddlewareMixin):

    def process_request(self, request):
        try:
            session = Session.objects.get(id=request.headers.get('Authorization', -1), expireAt__gte=datetime.now())
            request.account = NormalUser(session.pid)
        except Session.DoesNotExist:

            request.account = AnonymousUser

        logger.error(request.account)
        response = self.get_response(request)

        return response
