from rest_framework import serializers

from store.models import Store, Stock


class StoreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Store
        field = ['name', 'description', 'registerer', 'registerer_number', 'location', 'products']


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        field = '__all__'
