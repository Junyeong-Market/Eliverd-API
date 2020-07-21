from django.urls import path

from purchase.views import CreateOrderAPI, FailedOrderAPI

urlpatterns = [
    path('/', CreateOrderAPI.as_view()),
    # TODO: path('<oid>/'), order 조회
    # TODO: path('<oid>/approve/'), order 성공 (kp 전용)
    # TODO: path('<oid>/fail/'), order 실패 (kp 전용)
    path('<oid>/fail/', FailedOrderAPI.as_view()),  # order 실패 (kp 전용)
]
