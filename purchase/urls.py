from django.urls import path

from purchase.views import CreateOrderAPI

urlpatterns = [
    path('/', CreateOrderAPI.as_view()),
    # TODO: path('<oid>/'), order 조회
    # TODO: path('<oid>/approve/'), order 성공 (kp 전용)
    # TODO: path('<oid>/fail/'), order 실패 (kp 전용)
    # TODO: path('<oid>/cancel/'), order 취소 (kp 전용)
]
