from django.urls import path
from assets.views import FileUploadAPI

urlpatterns = [
    path('', FileUploadAPI.as_view())
]
