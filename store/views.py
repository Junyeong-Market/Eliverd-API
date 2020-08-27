import json
import logging

from django.contrib.gis.geos import Point
from django.core.exceptions import SuspiciousOperation
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response

from account.documentation.session import AuthorizationHeader
from account.pagination import AccountSearchPagination
from account.permissions import LoggedIn
from account.serializer import SafeUserSerializer
from product.models import Product
from product.serializer import ProductSerializer
from product.views import CreateProductAPI
from purchase.models import PartialOrder
from purchase.serializer import GetPartialOrderSerializer
from store.documentation import StoreInitBody, Lat, Lng, Distance, ModifyStockBody, Categories, ProductName
from store.models import Store, Stock
from store.pagination import StoreStockPagination
from store.serializer import StoreSerializer, StockSerializer, FlatStoreSerializer, FlatStockSerializer, \
    GetStockSerializer

logger = logging.getLogger(__name__)


class RadiusStoreList(ListAPIView):
    queryset = Store.objects.filter()
    serializer_class = StoreSerializer

    @swagger_auto_schema(operation_summary='범위 기반 상점 검색',
                         operation_description='지정된 범위 내의 상점을 가져옵니다.',
                         manual_parameters=[Lat, Lng, Distance])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        try:
            point = Point(float(self.request.query_params.get('lat')), float(self.request.query_params.get('lng')))
            return Store.objects.filter(location__distance_lte=(point, float(self.request.query_params.get('distance', 0))))
        except TypeError:
            raise SuspiciousOperation('Bad Request')


class StoreView(RetrieveAPIView):
    serializer_class = StoreSerializer

    @swagger_auto_schema(operation_summary='상점 정보 조회',
                         operation_description='지정한 상점의 정보를 가져옵니다.')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        return Store.objects.get(id=self.kwargs['id'])


class CreateStoreAPI(CreateAPIView):
    serializer_class = FlatStoreSerializer
    permission_classes = [LoggedIn]

    @swagger_auto_schema(operation_summary='상점 생성',
                         operation_description='상점을 생성합니다.',
                         request_body=StoreInitBody,
                         manual_parameters=[AuthorizationHeader],
                         responses={200: StoreSerializer})
    def post(self, request, *args, **kwargs):
        registerers = request.data.get('registerer')
        if isinstance(registerers, str):
            registerers = json.loads(registerers)
        request._full_data = {
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            'registerer': registerers,
            'registered_number': request.data.get('registered_number', ''),
            'location': Point(float(request.data.get('lat')), float(request.data.get('lng')))
        }
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer = StoreSerializer(serializer.instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class StoreStockListAPI(ListAPIView):
    queryset = Stock.objects.filter()
    serializer_class = GetStockSerializer
    pagination_class = StoreStockPagination

    @swagger_auto_schema(operation_summary='재고 목록 조회', operation_description='상점의 재고 목록을 조회합니다.',
                         manual_parameters=[Categories, ProductName])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        category = self.request.GET.get('category')
        if category:
            return Stock.objects.filter(store__id=self.kwargs['id'], amount__gt=0,
                                        product__name__contains=self.request.GET.get('name', ""),
                                        product__category=category)
        return Stock.objects.filter(store__id=self.kwargs['id'], amount__gt=0,
                                    product__name__contains=self.request.GET.get('name', ""))


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


class ModifyStockAPI(UpdateModelMixin, CreateAPIView):
    serializer_class = FlatStockSerializer

    @swagger_auto_schema(operation_summary='상점 재고 수정',
                         operation_description='상점에 재고를 추가/수정/삭제합니다.',
                         request_body=ModifyStockBody,
                         responses={200: FlatStockSerializer})
    def post(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = FlatStockSerializer(instance, data={
                'price': int(request.data.get('price', instance.price)),
                'amount': instance.amount + int(request.data.get('amount', 0))
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
        return Stock.objects.filter(store__id=int(self.kwargs['id']),
                                    product__ian=self.request.data.get('ian', -1))

    def get_object(self):
        return Stock.objects.get(store__id=int(self.kwargs['id']),
                                 product=Product.objects.get(ian=self.request.data.get('ian', 'notexist')))


class StoreOrderAPI(ListAPIView):
    serializer_class = GetPartialOrderSerializer
    pagination_class = AccountSearchPagination

    @swagger_auto_schema(operation_summary='상점 별 주문 내역 조회',
                         operation_description='각 상점이 처리해야 하는 주문 내역을 가져옵니다.')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return PartialOrder.objects.filter(store__id=self.kwargs['id']).order_by('-poid')


class StoreAdminAPI(ListAPIView, CreateAPIView, DestroyAPIView):
    serializer_class = SafeUserSerializer

    @swagger_auto_schema(operation_summary='상점 관리자 조회', operation_description='상점의 관리자 목록을 조회합니다.')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary='상정 관리자 추가', operation_description='상점에 관리자를 추가합니다.')
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary='상점 관리자 제거', operation_description='상점에서 관리자를 제거합니다.')
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Store.objects.get(id=self.kwargs['id']).registerer
