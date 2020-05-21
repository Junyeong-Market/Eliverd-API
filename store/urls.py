from rest_framework import routers

from store.views import RadiusStoreView, AreaStoreView

router = routers.SimpleRouter()

router.register(r'^by-radius/$', RadiusStoreView)
# router.register(r'^by-area/{area}/$', AreaStoreView)

urlpatterns = router.urls
