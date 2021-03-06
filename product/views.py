import logging

from django.contrib.gis.geos import Point
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import RetrieveAPIView, get_object_or_404, CreateAPIView, ListAPIView, UpdateAPIView

from account.documentation.session import AuthorizationHeader
from account.permissions import LoggedIn
from product.models import Product, Manufacturer
from product.pagination import ManufacturerSearchPagination
from product.serializer import ProductSerializer, ManufacturerSerializer
from store.documentation import Lat, Lng, Distance, ProductName, Categories, StockOrderBy
from store.models import Stock
from store.serializer import SafeStockSerializer

logger = logging.getLogger(__name__)


class GetProductAPI(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @swagger_auto_schema(operation_summary='상품 정보 조회',
                         operation_description='상품 정보를 가져옵니다.')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(Product, ian=self.kwargs['ian'])


class CreateProductAPI(CreateAPIView):
    serializer_class = ProductSerializer


class CreateManufacturerAPI(CreateAPIView):
    serializer_class = ManufacturerSerializer
    permission_classes = [LoggedIn]

    @swagger_auto_schema(operation_summary='제조사 생성',
                         operation_description='제조사를 생성합니다.',
                         manual_parameters=[AuthorizationHeader])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UpdateManufacturerAPI(UpdateAPIView):
    serializer_class = ManufacturerSerializer
    permission_classes = [LoggedIn]
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def get_queryset(self):
        return Manufacturer.objects.filter(pk=self.kwargs['id'])


class SearchManufacturerAPI(ListAPIView):
    serializer_class = ManufacturerSerializer
    pagination_class = ManufacturerSearchPagination

    @swagger_auto_schema(operation_summary='제조사 검색',
                         operation_description='지정한 문자열이 포함된 이름을 가진 제조사를 검색합니다.')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Manufacturer.objects.filter(name__contains=self.kwargs['name'])


class RadiusProductListAPI(ListAPIView):
    serializer_class = SafeStockSerializer

    @swagger_auto_schema(operation_summary='범위 기반 상품 검색',
                         operation_description='지정된 범위 내의 상품을 가져옵니다.',
                         manual_parameters=[Lat, Lng, Distance, Categories, ProductName, StockOrderBy])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        point = Point(float(self.request.query_params.get('lat')), float(self.request.query_params.get('lng')))
        distance = float(self.request.query_params.get('distance', 0))
        name = self.request.GET.get('name', "")
        order = self.request.GET.get('order_by', 'id')
        category = self.request.GET.get('category')
        stock = Stock.objects.filter(store__location__distance_lte=(point, distance), amount__gt=0,
                                     product__name__contains=name)
        if category:
            stock = stock.filter(product__category=category)

        return stock.order_by(order)


class RecommendedProductListAPI(ListAPIView):
    serializer_class = SafeStockSerializer

    @swagger_auto_schema(operation_summary='오늘의 상품 추천',
                         operation_description='지정된 범위 내의 상품을 가져옵니다.',
                         manual_parameters=[Lat, Lng])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        point = Point(float(self.request.query_params.get('lat', 0)), float(self.request.query_params.get('lng', 0)))

        return Stock.objects.order_by('?').filter(store__location__distance_lte=(point, 5), amount__gt=0)[:5]
