from rest_framework import serializers

from store.models import Store, Stock


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        depth = 1
        fields = '__all__'


class FlatStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'


class StoreInitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['name', 'description', 'registered_number', 'location']


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        depth = 2
        fields = '__all__'


class StockModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['price', 'amount']
