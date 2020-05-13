from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from account.serializer import UserSerializer


@api_view(['POST'])
def create_user(request):
    new_user = UserSerializer(data=request.data)
    if new_user.is_valid():
        new_user.save()
        return Response(new_user.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


