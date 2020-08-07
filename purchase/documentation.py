from drf_yasg import openapi

PgToken = openapi.Parameter(
    'pg_token',
    openapi.IN_QUERY,
    description='[KP] 카카오페이 거래 처리용 토큰',
    type=openapi.TYPE_STRING
)
