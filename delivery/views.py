from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import RetrieveAPIView

from delivery.documentations import DeliveryToken
from purchase.models import PartialOrder, OrderStatus
from purchase.serializer import GetPartialOrderSerializer


class StartDeliveryAPI(RetrieveAPIView):
    serializer_class = GetPartialOrderSerializer

    @swagger_auto_schema(operation_summary='배달 시작', operation_description='배달원이 배달할 주문을 등록합니다.',
                         manual_parameters=[DeliveryToken])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        p_order = PartialOrder.objects.get()
        p_order.transport = self.request.account.model
        p_order.status = OrderStatus.DELIVERING
        p_order.save()
        return p_order

