from drf_yasg import openapi

Asset = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(
            type=openapi.TYPE_INTEGER
        ),
        'image': openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_URI
        )
    }
)