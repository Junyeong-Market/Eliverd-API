from drf_yasg import openapi

SessionKey = openapi.Schema(
    '세션 키',
    description='세션 키',
    type=openapi.TYPE_STRING
)

SessionCreateSuccessful = openapi.Schema(
    '세션 생성됨',
    type=openapi.TYPE_OBJECT,
    properties={
        'session': SessionKey
    }
)

IDParameter = openapi.Schema(
    '아이디',
    description='유저의 아이디',
    type=openapi.TYPE_STRING
)

PWParameter = openapi.Schema(
    '비밀번호',
    description='유저의 비밀번호',
    type=openapi.TYPE_STRING
)

LoginRequestBody = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['user_id', 'password'],
    properties={
        'user_id': IDParameter,
        'password': PWParameter
    }
)

AuthorizationHeader = openapi.Parameter(
    'Authorization',
    openapi.IN_HEADER,
    description='세션 헤더',
    type=openapi.TYPE_STRING
)
