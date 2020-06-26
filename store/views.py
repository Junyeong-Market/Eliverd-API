import logging

from django.contrib.gis.geos import Point
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response

from product.models import Product
from product.serializer import ProductSerializer
from product.views import CreateProductAPI
from store.models import Store, Stock
from store.pagination import StoreStockPagination
from store.serializer import StoreSerializer, StockSerializer, StoreInitSerializer

logger = logging.getLogger(__name__)


class RadiusStoreList(ListAPIView):
    queryset = Store.objects.filter()
    serializer_class = StoreSerializer

    @swagger_auto_schema(operation_summary='범위 기반 상점 검색',
                         operation_description='지정된 범위 내의 상점을 가져옵니다.')
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

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
    serializer_class = StoreSerializer

    def get_object(self):
        return Store.objects.get(id=self.kwargs['id'])


class CreateStoreAPI(CreateAPIView):
    serializer_class = StoreSerializer

    @swagger_auto_schema(operation_summary='상점 생성',
                         operation_description='상점을 생성합니다.',
                         request_body=StoreInitSerializer,
                         responses={200: StoreSerializer})
    def post(self, request, *args, **kwargs):
        request._full_data = {
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            'registerer': [request.account.pid],
            'registerer_number': request.data.get('registerer_number') or '',
            'location': Point(request.data.get('lat'), request.data.get('lng'))
        }
        return super().post(request, *args, **kwargs)


class StoreStockListAPI(ListAPIView):
    queryset = Stock.objects.filter()
    serializer_class = StockSerializer
    pagination_class = StoreStockPagination

    def get_queryset(self):
        return Stock.objects.filter(id=self.kwargs['id'])


class AddStockAPI(CreateAPIView):
    serializer_class = StockSerializer

    def create(self, request, *args, **kwargs):
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


class ModifyStockAPI(UpdateModelMixin, CreateAPIView):
    serializer_class = StockSerializer

    def post(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = StockSerializer(instance,
                                         data={
                                             'price': request.data.get('price', instance.price),
                                             'amount': instance.amount + request.data.get('amount', 0)
                                         }, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except Product.DoesNotExist:
            serializer = ProductSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            product = serializer.instance
        except Stock.DoesNotExist:
            ian = request.data.get('ian', None)
            product = Product.objects.get(ian=ian)
        request._full_data = {
            'store': kwargs['id'],
            'product': product.id,
            'price': request.data.get('price'),
            'amount': request.data.get('amount')
        }
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        return Stock.objects.filter(store=self.kwargs['id'], product=self.request.data.get('ian', -1))

    def get_object(self):
        return Stock.objects.get(store=int(self.kwargs['id']),
                                 product=Product.objects.get(ian=self.request.data.get('ian', 'notexist')))


