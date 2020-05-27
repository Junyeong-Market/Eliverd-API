from django.urls import path
from account.views import UserInfoAPI, SessionAPI, RegisterAPI

urlpatterns = [
    path('session/', SessionAPI.as_view()),
    path('user/', RegisterAPI.as_view()),
    path('user/<pid>/', UserInfoAPI.as_view())
]
