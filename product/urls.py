from django.urls import path

from product.views import GetProductAPI, SearchManufacturerAPI, CreateManufacturerAPI, UpdateManufacturerAPI, \
    RecommendedProductListAPI, RadiusProductListAPI

urlpatterns = [
    path('manufacturer/', CreateManufacturerAPI.as_view()),
    path('manufacturer/<id>/', UpdateManufacturerAPI.as_view()),
    path('manufacturer/search/<name>/', SearchManufacturerAPI.as_view()),
    path('by-radius/', RadiusProductListAPI.as_view()),
    path('recommended/', RecommendedProductListAPI.as_view()),
    path('<ian>/', GetProductAPI.as_view()),
]