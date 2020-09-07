from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import RetrieveAPIView, get_object_or_404, ListAPIView

from account.documentation.session import AuthorizationHeader
from account.permissions import LoggedIn
from delivery.documentations import DeliveryToken
from purchase.models import PartialOrder, OrderStatus
from purchase.serializer import GetPartialOrderSerializer


class DeliveryHandlerAPI(RetrieveAPIView):
    serializer_class = GetPartialOrderSerializer

    @swagger_auto_schema(operation_summary='배달 토큰 핸들러', operation_description='배달 토큰을 처리합니다.',
                         manual_parameters=[DeliveryToken, AuthorizationHeader])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        p_order = get_object_or_404(PartialOrder, transport_token=self.request.GET.get('token', ''))
        if p_order.status == OrderStatus.READY:
            p_order.transport = self.request.account.model
            p_order.status = OrderStatus.DELIVERING
        elif p_order.status == OrderStatus.DELIVERING:
            p_order.status = OrderStatus.DELIVERED
            p_order.transport_token = None
        else:
            raise
        p_order.save()
        return p_order


class MyDeliveryJobAPI(RetrieveAPIView):
    serializer_class = GetPartialOrderSerializer
    permission_classes = [LoggedIn]

    @swagger_auto_schema(operation_summary='처리하고 있는 배달 가져오기', operation_description='유저가 처리하고 있는 배달을 가져옵니다.',
                         manual_parameters=[AuthorizationHeader])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        return PartialOrder.objects.get(transport=self.request.account.model, status=OrderStatus.DELIVERING)
