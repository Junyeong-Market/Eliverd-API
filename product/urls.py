from django.urls import path

from product.views import GetProductAPI

urlpatterns = [
    path('{ian}/', GetProductAPI.as_view())
]