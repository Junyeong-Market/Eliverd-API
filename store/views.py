from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from store.models import Store
from store.serializer import StoreSerializer


class RadiusStoreList(ListAPIView):
    queryset = Store.objects.filter()
    serializer_class = StoreSerializer

    def get_queryset(self):
        point = Point(self.request.query_params.get('lat'), self.request.query_params.get('lng'))
        distance = D(m=self.request.query_params.distance)
        return Store.objects.filter(location__distance_lte=(point, distance))

    @classmethod
    def get_extra_actions(cls):
        return []


# class AreaStoreView(ListAPIView):
#     queryset = Store.objects.filter()
#     serializer_class = StoreSerializer
#
#     def get_queryset(self):
#         return Store.objects.filter()

class StoreView(APIView):

    def get(self):
        return Response(Store.objects.get(id=self.kwargs['id']))


class StoreStockList(RetrieveAPIView):
    queryset = Store.objects.filter()
    serializer_class = StoreSerializer
    lookup_field = 'products'

    def get_queryset(self):
        return Store.objects.filter(id=self.kwargs['id'])
