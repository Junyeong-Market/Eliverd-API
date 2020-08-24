from rest_framework import serializers

from purchase.models import OrderedStock, Order, PartialOrder


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
        depth = 4
        fields = '__all__'
