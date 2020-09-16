from django.urls import path
from assets.views import FileUploadAPI, GetAssetAPI

urlpatterns = [
    path('', FileUploadAPI.as_view()),
    path('<id>/', GetAssetAPI.as_view())
]
