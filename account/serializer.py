from account.models import User, Session
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'password', 'realname', 'nickname', 'is_seller']


class SafeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        depth = 2
        fields = ['pid', 'user_id', 'nickname', 'realname', 'is_seller']


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname', 'realname', 'is_seller']


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'pid']
