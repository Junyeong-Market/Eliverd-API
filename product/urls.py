from django.urls import path

from product.views import GetProductAPI, SearchManufacturerAPI, CreateManufacturerAPI

urlpatterns = [
    path('manufacturer/', CreateManufacturerAPI.as_view()),
    path('manufacturer/search/<name>/', SearchManufacturerAPI.as_view()),
    path('<ian>/', GetProductAPI.as_view()),
]