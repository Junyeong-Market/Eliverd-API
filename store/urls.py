from django.urls import path

from store.views import RadiusStoreList, StoreStockListAPI, StoreView, AddStockAPI, RemoveStockAPI, CreateStoreAPI

urlpatterns = [
    path('', CreateStoreAPI.as_view()),
    path('by-radius/', RadiusStoreList.as_view()),
    path('<id>/', StoreView.as_view()),
    path('<id>/stocks', StoreStockListAPI.as_view()),
    path('<id>/stock', AddStockAPI.as_view()),
    path('<id>/stock/<product>', RemoveStockAPI.as_view())
]
