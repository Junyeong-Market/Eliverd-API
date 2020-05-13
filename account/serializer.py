from account.models import User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        field = ['pid', 'id', 'password', 'nickname', 'isSeller']


class SessionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        field = ['pid', 'id', 'password', 'nickname', 'isSeller']
