from django.urls import path
from account.views import UserInfoAPI, SessionAPI, RegisterAPI, UserDataVerifyAPI, UserSearchAPI

urlpatterns = [
    path('session/', SessionAPI.as_view()),
    path('user/', RegisterAPI.as_view()),
    path('user/validate/', UserDataVerifyAPI.as_view()),
    path('user/search/<name>/', UserSearchAPI.as_view()),
    path('user/<pid>/', UserInfoAPI.as_view())
]
