from django.urls import path

from purchase.views import CreateOrderAPI, FailedOrderAPI, CancelOrderAPI, GetOrderAPI, SuccessOrderAPI

urlpatterns = [
    path('', CreateOrderAPI.as_view()),
    path('<oid>/', GetOrderAPI.as_view()),  # order 조회
    path('<oid>/approve/', SuccessOrderAPI.as_view()),  # order 성공 (kp 전용)
    path('<oid>/fail/', FailedOrderAPI.as_view()),  # order 실패 (kp 전용)
    path('<oid>/cancel/', CancelOrderAPI.as_view()),  # order 취소 (kp 전용)
]
