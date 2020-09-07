from django.urls import path

from delivery.views import DeliveryHandlerAPI

urlpatterns = [
    path('/', DeliveryHandlerAPI.as_view()),
    path('processing/', MyDeliveryJobAPI.as_view())
]
