from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import RetrieveAPIView, get_object_or_404, CreateAPIView, ListAPIView

from product.models import Product, Manufacturer
from product.pagination import ManufacturerSearchPagination
from product.serializer import ProductSerializer, ManufacturerSerializer


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
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class SearchManufacturerAPI(ListAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    pagination_class = ManufacturerSearchPagination

    @swagger_auto_schema(operation_summary='제조사 검색',
                         operation_description='지정한 문자열이 포함된 이름을 가진 제조사를 검색합니다.')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Manufacturer.objects.filter(name__contains=self.kwargs['name'])
