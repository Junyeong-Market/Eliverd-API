from django.contrib.gis.geos import Point
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from store.models import Store, Stock
from store.serializer import StoreSerializer, StockSerializer


class RadiusStoreList(ListAPIView):
    queryset = Store.objects.filter()
    serializer_class = StoreSerializer

    def get_queryset(self):
        point = Point(float(self.request.query_params.get('lat')), float(self.request.query_params.get('lng')))
        return Store.objects.filter(location__distance_lte=(point, float(self.request.query_params.get('distance'))))

    @classmethod
    def get_extra_actions(cls):
        return []


# class AreaStoreView(ListAPIView):
#     queryset = Store.objects.filter()
#     serializer_class = StoreSerializer
#
#     def get_queryset(self):
#         return Store.objects.filter()

class StoreView(RetrieveAPIView):

    def get_object(self):
        return Store.objects.get(id=self.kwargs['id'])


class StoreStockListAPI(ListAPIView):
    queryset = Stock.objects.filter()
    serializer_class = StockSerializer

    def get_queryset(self):
        return Store.objects.filter(id=self.kwargs['id'])
