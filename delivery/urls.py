from django.urls import path

from delivery.views import DeliveryHandlerAPI, MyDeliveryJobAPI

urlpatterns = [
    path('/', DeliveryHandlerAPI.as_view()),
    path('processing/', MyDeliveryJobAPI.as_view())
]
