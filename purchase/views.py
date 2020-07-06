import os

import requests

from rest_framework.generics import CreateAPIView


class CreateOrderAPI(CreateAPIView):
    def post(self, request, *args, **kwargs):
        res = super().post(request, *args, **kwargs)
        oid = res.data['oid']
        requests.post('https://kapi.kakao.com/v1/payment/ready',
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

