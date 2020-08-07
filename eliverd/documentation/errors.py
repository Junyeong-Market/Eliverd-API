from drf_yasg import openapi

# DRF Serializer 검증 중에 발생하는 오류입니다.
VerificationError = openapi.Schema(
    'Django ORM 에러 문자열',
    type=openapi.TYPE_STRING,
    enum=[
        'user with this {data_name} already exists.',
        'Ensure this field has {data_error}'
    ]
)

# 이 오류는 Array 형태로 반환됩니다.
ErrorArray = openapi.Schema(
    description='데이터에 대한 오류를 출력합니다.',
    type=openapi.TYPE_ARRAY,
    items=VerificationError
)