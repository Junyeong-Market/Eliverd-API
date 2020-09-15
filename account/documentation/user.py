from drf_yasg import openapi

from account.documentation.session import IDParameter, PWParameter
from eliverd.documentation.errors import ErrorArray
from store.documentation import Store

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

Month = openapi.Parameter(
    'month',
    openapi.IN_QUERY,
    type=openapi.TYPE_INTEGER,
    description='몇 달 전까지 조회할지 지정합니다.'
)

UserSummaryResponse = openapi.Response(
    description='유저의 총 구매 횟수와 총액입니다.',
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'count': openapi.Schema(
                description='구매 횟수',
                type=openapi.TYPE_INTEGER
            ),
            'total': openapi.Schema(
                description='구매 총액',
                type=openapi.TYPE_INTEGER
            ),
        }
    )
)

SessionUserResponse = openapi.Response(
    description='세션 유저 조회 데이터',
    schema=openapi.Schema(
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
            'stores': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=Store
            )
        }
    )
)

IsActive = openapi.Parameter(
    'is_active',
    openapi.IN_QUERY,
    type=openapi.TYPE_BOOLEAN,
    description='지금 배달 중인 주문만 조회합니다.'
)