import hashlib
import logging

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, RetrieveDestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from account.documentation.session import SessionCreateSuccessful, AuthorizationHeader
from account.documentation.user import UserSearchParameter
from account.models import Session, User
from account.pagination import AccountSearchPagination
from account.permissions import NotLoggedIn, LoggedIn
from account.serializer import UserSerializer, SessionSerializer, SafeUserSerializer
from store.models import Store

logger = logging.getLogger(__name__)


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


class SessionAPI(CreateAPIView, RetrieveDestroyAPIView):
    serializer_class = SessionSerializer
    lookup_field = 'id'

    @swagger_auto_schema(operation_summary='세션 생성 (로그인)',
                         operation_description='로그인 정보를 보내서 세션을 생성합니다.',
                         responses={
                             200: SessionCreateSuccessful
                         })
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

    @swagger_auto_schema(operation_summary='세션 삭제 (로그아웃)',
                         operation_description='현재 세션을 삭제합니다.',
                         manual_parameters=[AuthorizationHeader])
    @permission_classes([LoggedIn])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary='세션 정보 조회',
                         operation_description='현재 세션 유저의 정보를 조회합니다.',
                         manual_parameters=[AuthorizationHeader],
                         responses={
                             200: SafeUserSerializer
                         })
    @permission_classes([LoggedIn])
    def get(self, request, *args, **kwargs):
        session = self.get_object()
        serializer = SafeUserSerializer(session.pid)
        stores = Store.objects.filter(registerer=session.pid)
        stores = [store.id for store in stores]
        data = serializer.data
        data.update({"stores": stores})
        return Response(data)

    def get_object(self):
        try:
            return Session.objects.get(id=self.request.headers.get('Authorization'))
        except Session.DoesNotExist:
            raise PermissionDenied


class UserDataVerifyAPI(APIView):
    permission_classes = [NotLoggedIn]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class UserSearchAPI(ListAPIView):
    serializer_class = SafeUserSerializer
    pagination_class = AccountSearchPagination

    @swagger_auto_schema(operation_summary='사용자 검색', operation_description='특정 문자열이 포함된 이름을 가지고 있는 유저를 검색힙니다',
                         manual_parameters=[UserSearchParameter])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        is_seller = self.request.query_params.get('is_seller', None)
        if is_seller:
            return User.objects.filter(realname__contains=self.kwargs['name'], is_seller=is_seller)
        return User.objects.filter(realname__contains=self.kwargs['name'])
