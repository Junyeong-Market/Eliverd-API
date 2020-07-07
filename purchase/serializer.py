from rest_framework import serializers

from purchase.models import OrderedStock, Order


class OrderedStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedStock
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
