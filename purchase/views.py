import json
import os
import logging

import requests
from django.contrib.gis.geos import Point
from drf_yasg.utils import swagger_auto_schema

from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response

from account.documentation.session import AuthorizationHeader
from account.permissions import LoggedIn
from purchase.documentation import PgToken, CreateOrderBody, CreateOrderResponse
from purchase.models import Order, OrderStatus, StockAppliedStatus, TransactionStatus
from purchase.serializer import OrderedStockSerializer, OrderSerializer, PartialOrderSerializer, GetOrderSerializer

logger = logging.getLogger(__name__)


class GetOrderAPI(RetrieveAPIView):
    serializer_class = GetOrderSerializer

    @swagger_auto_schema(operation_summary='주문 조회', operation_description='주문을 조회합니다.')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        return Order.objects.get(oid=self.kwargs['oid'])


class CreateOrderAPI(CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [LoggedIn]

    @swagger_auto_schema(operation_summary='주문 생성', operation_description='여러 상점에 주문을 신청합니다.',
                         manual_parameters=[AuthorizationHeader], request_body=CreateOrderBody,
                         responses={200: CreateOrderResponse})
    def post(self, request, *args, **kwargs):
        destination = request.data.get('deliver_to', None)
        destination = Point(float(destination.get('lat')), float(destination.get('lng')))\
            if destination is not None else None
        orders = []
        for order in request.data['orders']:
            stocks = order.get('stocks')
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
                'stocks': stocks,
                'destination': destination
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
            'destination': destination
        })
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        order = serializer.instance
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
                                     'approval_url': f"{host}/purchase/{oid}/approve/",
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


class SuccessOrderAPI(RetrieveAPIView):
    serializer_class = GetOrderSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.order = None

    @swagger_auto_schema(operation_summary='주문 성공 핸들러 [KP]', operation_description='카카오페이 주문 성공 핸들러',
                         manual_parameters=[PgToken])
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        requests.post('https://kapi.kakao.com/v1/payment/approve',
                      data={
                          'cid': os.getenv('KAKAOPAY_CID'),
                          'tid': self.order.tid,
                          'partner_order_id': self.order.oid,
                          'partner_user_id': self.order.customer.pid,
                          'pg_token': request.GET['pg_token']
                      },
                      headers={
                          'Authorization': f"KakaoAK {os.getenv('KAKAO_ADMIN')}"
                      })
        return response

    def get_object(self):
        order = Order.objects.get(oid=self.kwargs['oid'])
        for partial in order.partials.all():
            for stock in partial.stocks.all():
                stock.status = StockAppliedStatus.APPLIED
                stock.stock.amount = stock.stock.amount - stock.amount
                result = stock.stock.save()
                logger.info(result)
                stock.save()
            partial.status = OrderStatus.READY if order.destination else OrderStatus.DONE
        order.status = TransactionStatus.PROCESSED
        order.save()
        self.order = order
        return self.order


class CancelOrderAPI(RetrieveAPIView):
    serializer_class = GetOrderSerializer

    @swagger_auto_schema(operation_summary='주문 취소 핸들러 [KP]', operation_description='카카오페이 주문 취소 핸들러')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        order = Order.objects.get(oid=self.kwargs['oid'])
        for partial in order.partials.all():
            for stock in partial.stocks.all():
                stock.status = StockAppliedStatus.FAILED
                stock.save()
            partial.status = OrderStatus.CANCELED
            partial.save()
        order.status = TransactionStatus.CANCELED
        order.save()
        return order


class FailedOrderAPI(RetrieveAPIView):
    serializer_class = GetOrderSerializer

    @swagger_auto_schema(operation_summary='주문 실패 핸들러 [KP]', operation_description='카카오페이 주문 실패 핸들러')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        order = Order.objects.get(oid=self.kwargs['oid'])
        for partial in order.partials.all():
            for stock in partial.stocks.all():
                stock.status = StockAppliedStatus.FAILED
                stock.save()
            partial.status = OrderStatus.CANCELED
            partial.save()
        order.status = TransactionStatus.FAILED
        order.save()
        return order


class ContinueOrderAPI(RetrieveAPIView):
    serializer_class = GetOrderSerializer
    permission_classes = [LoggedIn]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @swagger_auto_schema(operation_summary='주문 계속 진행', operation_description='취소/실패한 주문을 다시 진행합니다.',
                         manual_parameters=[AuthorizationHeader], responses={200: CreateOrderResponse})
    def get(self, request, *args, **kwargs):
        order = self.get_object()
        if order.status == TransactionStatus.PROCESSED:
            return Response(400)
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
                                     'approval_url': f"{host}/purchase/{oid}/approve/",
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

    def get_object(self):
        order = Order.objects.get(oid=self.kwargs['oid'])
        if order.status == TransactionStatus.PROCESSED:
            return order
        for partial in order.partials.all():
            for stock in partial.stocks.all():
                stock.status = StockAppliedStatus.PREPARED
                stock.stock.amount = stock.stock.amount - stock.amount
                result = stock.stock.save()
                logger.info(result)
                stock.save()
            partial.status = OrderStatus.PENDING
        order.status = TransactionStatus.PENDING
        order.save()
        return order
