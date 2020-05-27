import hashlib

from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import Session, User
from account.permissions import NotLoggedIn, LoggedIn
from account.serializer import UserSerializer, SessionSerializer


class RegisterAPI(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [NotLoggedIn]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return Response(status=response.status_code)


class UserInfoAPI(APIView):
    permission_classes = [LoggedIn]

    def post(self, request, pid):
        if request.account.pid != pid:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = UserSerializer(request.account, data=request.data)

        if serializer.is_valid():
            serializer.save()
        return Response({'data': serializer.data})

    def delete(self, request, pid):
        if request.account.pid != pid:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_200_OK)


class SessionAPI(CreateAPIView, DestroyAPIView):
    serializer_class = SessionSerializer
    lookup_field = 'id'

    @permission_classes([NotLoggedIn])
    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(user_id=request.data.get('user_id'),
                                    password=hashlib.sha512(str(request.data.get('password'))
                                                            .encode('utf-8')).hexdigest())
            request._full_data = {'pid': user.pid}
            response = super().post(request, *args, **kwargs)
            response.data = {'session': response.data.get('id')}
            return response
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @permission_classes([LoggedIn])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_object(self):
        try:
            return Session.objects.get(id=self.request.headers.get('Authorization'))
        except Session.DoesNotExist:
            raise PermissionDenied
