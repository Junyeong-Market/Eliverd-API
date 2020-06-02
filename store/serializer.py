from rest_framework import serializers

from store.models import Store, Stock


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        field = ['name', 'description', 'registerer', 'registerer_number', 'location']


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        field = '__all__'
