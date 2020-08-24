from rest_framework import serializers

from account.serializer import SafeUserSerializer
from purchase.models import OrderedStock, Order, PartialOrder
from store.serializer import StoreSerializer, GetStockSerializer


class OrderedStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedStock
        fields = '__all__'


class PartialOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartialOrder
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class DeepOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        depth = 5
        fields = '__all__'


class GetOrderedStockSerializer(serializers.ModelSerializer):
    stock = GetStockSerializer()

    class Meta:
        model = OrderedStock
        fields = '__all__'


class GetPartialOrderSerializer(serializers.ModelSerializer):
    store = StoreSerializer()
    stocks = GetOrderedStockSerializer(many=True)

    class Meta:
        model = PartialOrder
        fields = '__all__'


class GetOrderSerializer(serializers.ModelSerializer):
    customer = SafeUserSerializer()
    partials = GetPartialOrderSerializer(many=True)

    class Meta:
        model = Order
        depth = 5
        fields = '__all__'
