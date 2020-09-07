from django.urls import path
from account.views import UserInfoAPI, SessionAPI, RegisterAPI, UserDataVerifyAPI, UserSearchAPI, UserOwnedStoreAPI, \
    UserOrderAPI, UserOrderSummaryAPI, DeliveryListAPI

urlpatterns = [
    path('session/', SessionAPI.as_view()),
    path('user/', RegisterAPI.as_view()),
    path('user/validate/', UserDataVerifyAPI.as_view()),
    path('user/search/<name>/', UserSearchAPI.as_view()),
    path('user/<pid>/', UserInfoAPI.as_view()),
    path('user/<pid>/stores/', UserOwnedStoreAPI.as_view()),
    path('user/<pid>/orders/', UserOrderAPI.as_view()),
    path('user/<pid>/summary/', UserOrderSummaryAPI.as_view()),
    path('user/<pid>/deliveries/', DeliveryListAPI.as_view())
]
