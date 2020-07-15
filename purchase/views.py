import json
import os

import requests

from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from account.permissions import LoggedIn
from purchase.serializer import OrderedStockSerializer, OrderSerializer, PartialOrderSerializer


class CreateOrderAPI(CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [LoggedIn]

    def post(self, request, *args, **kwargs):
        '''

        :param request:
        {
            store: 0,
            stock: [{
                id: id,
                amount: 0
            }]
        }
        :param args:
        :param kwargs:
        :return:
        '''
        orders = []
        for order in request.data:
            stocks = request.data.get('stock')
            serializers = []
            for stock in stocks:
                serializer = OrderedStockSerializer(data={
                    'stock': stock.id,
                    'amount': stock.amount
                })
                serializer.is_valid(raise_exception=True)
                serializers.append(serializer)
            for serializer in serializers:
                serializer.save()
            stocks = [serializer.instance.id for serializer in serializers]
            # OrderedStock 생성

            serializer = PartialOrderSerializer(data={
                'store': request.data.get('store'),
                'stock': stocks
            })
            serializer.is_valid(raise_exception=True)
            orders.append(serializer)
        for order in orders:
            order.save()
        orders = [serializer.instance.poid for serializer in orders]
        # OrderedStock 생성

        request._full_body = {
            'customer': request.account.pid,
            'partials': orders,
        }

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        instance = serializer.instance
        oid = instance.oid
        response = requests.post('https://kapi.kakao.com/v1/payment/ready',
                                 data={
                                     'cid': os.getenv('KAKAOPAY_CID'),
                                     'partner_order_id': oid,
                                     'partner_user_id': request.account.pid,
                                     'item_name': instance.store.name,
                                     'quantity': 1,
                                     'total_amount': instance.total,
                                     'vat_amount': instance.total / 11,
                                     'tax_free_amount': instance.total - instance.total / 11,
                                     'approval_url': f"/purchase/{oid}/success/",
                                     'fail_url': f"/purchase/{oid}/fail/",
                                     'cancel_url': f"/purchase/{oid}/cancel/"
                                 },
                                 headers={
                                     'Authorization': f"KakaoAK {os.getenv('KAKAO_ADMIN')}"
                                 })

        response = json.loads(response.text)
        response['oid'] = oid

        # response tid로 Order 업데이트
        serializer = self.get_serializer(instance, data=response, partial=True)
        serializer.save()

        return Response(response, status=201)
