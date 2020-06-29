from drf_yasg import openapi

from account.documentation.session import IDParameter, PWParameter
from eliverd.docs.errors import ErrorArray

UserSearchParameter = openapi.Parameter(
    'is_seller',
    openapi.IN_QUERY,
    description='검색할 대상이 판매자인지 일반인인지 구분합니다.',
    type=openapi.TYPE_BOOLEAN
)

LoginRequestBody = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'user_id': IDParameter,
        'password': PWParameter
    }
)

UserDataErrorSchema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'realname': ErrorArray,
        'nickname': ErrorArray,
        'user_id': ErrorArray,
        'password': ErrorArray
    }
)

UserDataErrorResponse = openapi.Response(
    type=openapi.TYPE_OBJECT,
    description='유저 데이터에 오류가 있을 시 오류를 반환합니다.',
    schema=UserDataErrorSchema
)