import os

import requests

from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from purchase.serializer import OrderedStockSerializer


class CreateOrderAPI(CreateAPIView):
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
        # OrderedStock 생성

        res = super().post(request, *args, **kwargs)  # Order 생성

        oid = res.data['oid']
        response = requests.post('https://kapi.kakao.com/v1/payment/ready',
                                 data={
                                     'cid': os.getenv('KAKAOPAY_CID'),
                                     'partner_order_id': oid,
                                     'partner_user_id': request.account.pid,
                                     'item_name': 'some name',
                                     'quantity': 1,
                                     'total_amount': 0,
                                     'vat_amount': 'total_amount / 11',
                                     'tax_free_amount': 0,
                                     'approval_url': f"/purchase/{oid}/success/",
                                     'fail_url': f"/purchase/{oid}/fail/",
                                     'cancel_url': f"/purchase/{oid}/cancel/"
                                 },
                                 headers={
                                     'Authorization': f"KakaoAK {os.getenv('KAKAO_ADMIN')}"
                                 })

        # response tid로 Order 업데이트

        return Response(response.text)
