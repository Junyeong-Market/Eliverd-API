from drf_yasg import openapi

from account.documentation.session import IDParameter

SafeUser = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'pid': openapi.Schema(
            type=openapi.TYPE_INTEGER
        ),
        'user_id': IDParameter,
        'nickname': openapi.Schema(
            type=openapi.TYPE_STRING
        ),
        'realname': openapi.Schema(
            type=openapi.TYPE_STRING
        ),
        'is_seller': openapi.Schema(
            type=openapi.TYPE_BOOLEAN
        )
    }
)
