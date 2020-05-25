from rest_framework import routers

from store.views import RadiusStoreView, StoreStockView

router = routers.SimpleRouter()

router.register(r'^by-radius/$', RadiusStoreView)
# router.register(r'^by-area/{area}/$', AreaStoreView)
router.register(r'^(?P<id>.+)/stocks$', StoreStockView)

urlpatterns = router.urls
