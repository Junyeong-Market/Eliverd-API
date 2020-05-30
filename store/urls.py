from django.urls import path

from store.views import RadiusStoreList, StoreStockListAPI, StoreView

urlpatterns = [
    path('by-radius/', RadiusStoreList.as_view()),
    path('{id}/', StoreView.as_view()),
    path('{id}/stocks', StoreStockListAPI.as_view()),
]
