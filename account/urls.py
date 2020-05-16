from django.urls import path
from account.views import UserInfoAPI, SessionAPI, create_user

urlpatterns = [
    path('session/', SessionAPI.as_view()),
    path('user/', create_user),
    path('user/<pid>/', UserInfoAPI.as_view())
]
