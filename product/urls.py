from django.urls import path

from product.views import GetProductAPI, SearchManufacturerAPI

urlpatterns = [
    path('<ian>/', GetProductAPI.as_view()),
    path('manufacturer/search/<name>/', SearchManufacturerAPI.as_view())
]