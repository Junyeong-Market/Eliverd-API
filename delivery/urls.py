from django.urls import path

from delivery.views import StartDeliveryAPI

urlpatterns = [
    path('start/', StartDeliveryAPI.as_view()),
]
