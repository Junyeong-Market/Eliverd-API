from rest_framework import routers

from store.views import RadiusStoreView

router = routers.SimpleRouter()

router.register(r'^by-radius/$', RadiusStoreView)

urlpatterns = router.urls
