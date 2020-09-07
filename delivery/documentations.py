from drf_yasg import openapi

DeliveryToken = openapi.Parameter(
    'token',
    openapi.IN_QUERY,
    type=openapi.TYPE_STRING,
    format=openapi.FORMAT_UUID
)
