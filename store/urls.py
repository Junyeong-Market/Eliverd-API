from django.urls import path
from rest_framework import routers

from store.views import RadiusStoreList, StoreStockList, StoreView

router = routers.SimpleRouter()

router.register(r'^by-radius/$', RadiusStoreList)
# router.register(r'^by-area/{area}/$', AreaStoreView)
router.register(r'^(?P<id>.+)/stocks$', StoreStockList)

urlpatterns = [
    path('by-radius/', RadiusStoreList.as_view()),
    path('{id}/', StoreView.as_view()),
    path('{id}/stocks', StoreStockList.as_view())
]
