from rest_framework.generics import RetrieveAPIView, get_object_or_404, CreateAPIView

from product.models import Product
from product.serializer import ProductSerializer


class GetProductAPI(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_object(self):
        return get_object_or_404(Product, ian=self.kwargs['ian'])


class CreateProductAPI(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
