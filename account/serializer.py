from account.models import User, Session
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class SafeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        depth = 2
        exclude = ['password']


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password', 'nickname', 'realname', 'home', 'profile']


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'pid']
