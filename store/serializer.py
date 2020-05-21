from rest_framework import serializers

from store.models import Store


class StoreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Store
        field = ['name', 'description', 'registerer', 'registerer_number', 'location', 'products']
