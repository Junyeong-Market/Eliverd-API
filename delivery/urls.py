from django.urls import path

from delivery.views import StartDeliveryAPI, ReceiveDeliveryAPI

urlpatterns = [
    path('start/', StartDeliveryAPI.as_view()),
    path('receive/', ReceiveDeliveryAPI.as_view()),
]
