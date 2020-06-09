from django.contrib.gis.geos import Point
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView

from product.models import Product
from product.views import CreateProductAPI
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


class CreateStoreAPI(CreateAPIView):

    def post(self, request, *args, **kwargs):
        request._full_data = {
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            'registerer': request.account.pid,
            'registerer_number': request.data.get('registerer_number'),
            'location': Point(request.data.get('lat'), request.data.get('lng'))
        }
        return super().post(request, *args, **kwargs)


class StoreStockListAPI(ListAPIView):
    queryset = Stock.objects.filter()
    serializer_class = StockSerializer

    def get_queryset(self):
        return Stock.objects.filter(id=self.kwargs['id'])


class AddStockAPI(CreateAPIView):
    serializer_class = StockSerializer

    def post(self, request, *args, **kwargs):
        ian = request.data.get('ian', None)
        if request.data.get('name', True):
            response = CreateProductAPI.post(request, *args, **kwargs)
            ian = response.data.ian
        # TODO: somehow manually generate ian

        product = Product.objects.get(ian=ian)

        request._full_data = {
            'store': kwargs['id'],
            'product': product.id,
            'price': request.data.get('price'),
            'amount': request.data.get('amount')
        }
        return super().post(request, *args, **kwargs)


class RemoveStockAPI(DestroyAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    def get_queryset(self):
        return Stock.objects.filter(store=self.kwargs['id'], product=self.kwargs['product'])
