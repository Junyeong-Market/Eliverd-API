from django.conf.urls import url
from django.urls import include, path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Eliverd API",
      default_version='v1',
      description="Eliverd API 문서",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="me@startergate.dev"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('account/', include('account.urls')),
    path('product/', include('product.urls')),
    path('purchase/', include('purchase.urls')),
    path('store/', include('store.urls'))
]
