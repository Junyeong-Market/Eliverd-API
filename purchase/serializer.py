from rest_framework import serializers

from account.serializer import SafeUserSerializer
from purchase.models import OrderedStock, Order, PartialOrder
from store.serializer import GetStockSerializer, StoreSerializer


class OrderedStockSerializer(serializers.ModelSerializer):
    stock = GetStockSerializer()

    class Meta:
        model = OrderedStock
        fields = '__all__'


class PartialOrderSerializer(serializers.ModelSerializer):
    stocks = OrderedStockSerializer(many=True)
    store = StoreSerializer()

    class Meta:
        model = PartialOrder
        fields = '__all__'
        depth = 2


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class DeepOrderSerializer(serializers.ModelSerializer):
    partials = PartialOrderSerializer(many=True)
    customer = SafeUserSerializer()

    class Meta:
        model = Order
        depth = 4
        fields = '__all__'
