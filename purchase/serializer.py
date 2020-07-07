from rest_framework import serializers

from purchase.models import OrderedStock


class OrderedStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedStock
        fields = '__all__'
