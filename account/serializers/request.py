from rest_framework import serializers

from account.models import User


class UserSearchRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_seller']

