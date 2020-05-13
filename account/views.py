from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import NotLoggedIn, LoggedIn
from account.serializer import UserSerializer


@api_view(['POST'])
@authentication_classes([NotLoggedIn])
def create_user(request):
    """
    Create New User
    :return: Created User
    """
    new_user = UserSerializer(data=request.data)
    if new_user.is_valid():
        new_user.save()
        return Response({'data': new_user.data}, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


class UserInfoAPI(APIView):
    permission_classes = [LoggedIn]

    def put(self, request, pid):
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


class SessionAPI(APIView):
    @permission_classes([NotLoggedIn])
    def post(self, request):
        return Response()

    @permission_classes([LoggedIn])
    def delete(self, request):
        return Response()
