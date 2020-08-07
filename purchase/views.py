import json
import os
import logging

import requests
from drf_yasg.utils import swagger_auto_schema

from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response

from account.permissions import LoggedIn
from purchase.models import Order, OrderStatus, StockAppliedStatus, TransactionStatus
from purchase.serializer import OrderedStockSerializer, OrderSerializer, PartialOrderSerializer

logger = logging.getLogger(__name__)


class GetOrderAPI(RetrieveAPIView):
    serializer_class = OrderSerializer

    @swagger_auto_schema(operation_summary='주문 조회', operation_description='주문을 조회합니다.')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        return Order.objects.filter(oid=self.kwargs['oid'])


class CreateOrderAPI(CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [LoggedIn]

    def post(self, request, *args, **kwargs):
        """
        :param request:
        {
            store: 0,
            stock: [{
                id: id,
                amount: 0
            }]
        }
        """
        orders = []
        for order in request.data:
            stocks = order.get('stock')
            serializers = []
            for stock in stocks:
                serializer = OrderedStockSerializer(data={
                    'stock': stock['id'],
                    'amount': stock['amount']
                })
                serializer.is_valid(raise_exception=True)
                serializers.append(serializer)
            for serializer in serializers:
                serializer.save()
            stocks = [serializer.instance.osid for serializer in serializers]
            # OrderedStock 생성

            serializer = PartialOrderSerializer(data={
                'store': order.get('store'),
                'stocks': stocks
            })
            serializer.is_valid(raise_exception=True)
            orders.append(serializer)
        for order in orders:
            order.save()
        # PartialOrder 생성
        orders = [serializer.instance.poid for serializer in orders]

        serializer = self.get_serializer(data={
            'customer': request.account.pid,
            'partials': orders,
        })
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        order = serializer.instance
        logger.info(order)
        oid = order.oid
        total = order.get_total()
        vat = int(total / 11)
        host = f"http://{request.META['HTTP_HOST']}"
        response = requests.post('https://kapi.kakao.com/v1/payment/ready',
                                 data={
                                     'cid': os.getenv('KAKAOPAY_CID'),
                                     'partner_order_id': oid,
                                     'partner_user_id': request.account.pid,
                                     'item_name': order.get_order_name(),
                                     'quantity': 1,
                                     'total_amount': total,
                                     'vat_amount': vat,
                                     'tax_free_amount': total - vat,
                                     'approval_url': f"{host}/purchase/{oid}/success/",
                                     'fail_url': f"{host}/purchase/{oid}/fail/",
                                     'cancel_url': f"{host}/purchase/{oid}/cancel/"
                                 },
                                 headers={
                                     'Authorization': f"KakaoAK {os.getenv('KAKAO_ADMIN')}"
                                 })

        response = json.loads(response.text)
        response['oid'] = oid

        # response tid로 Order 업데이트
        serializer = self.get_serializer(order, data=response, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(response, status=201)


class CancelOrderAPI(RetrieveAPIView):
    serializer_class = OrderSerializer

    @swagger_auto_schema(operation_summary='주문 취소 핸들러 [KP]', operation_description='카카오페이 주문 취소 핸들러')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        order = Order.objects.get(oid=self.kwargs['oid'])
        for partial in order.partials:
            for stock in partial.stocks:
                stock.status = StockAppliedStatus.FAILED
                stock.save()
            partial.status = OrderStatus.CANCELED
            partial.save()
        order.status = TransactionStatus.CANCELED
        order.save()
        return order


class FailedOrderAPI(RetrieveAPIView):
    serializer_class = OrderSerializer

    @swagger_auto_schema(operation_summary='주문 실패 핸들러 [KP]', operation_description='카카오페이 주문 실패 핸들러')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        order = Order.objects.get(oid=self.kwargs['oid'])
        for partial in order.partials:
            for stock in partial.stocks:
                stock.status = StockAppliedStatus.FAILED
                stock.save()
            partial.status = OrderStatus.CANCELED
            partial.save()
        order.status = TransactionStatus.FAILED
        order.save()
        return order
