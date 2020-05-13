from account.models import User, Session


class AuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        pid = Session.objects.filter(id=request.headers.get('Authorization'))

        request.user = User.objects.filter(pid=pid)

        response = self.get_response(request)

        return response
