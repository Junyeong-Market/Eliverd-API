from drf_yasg import openapi

UserSearchParameter = openapi.Parameter(
    'is_seller',
    openapi.IN_QUERY,
    description='검색할 대상이 판매자인지 일반인인지 구분합니다.',
    type=openapi.TYPE_BOOLEAN
)