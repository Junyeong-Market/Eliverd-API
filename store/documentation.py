from drf_yasg import openapi

StoreNameParameter = openapi.Schema(
    description='상점 이름',
    type=openapi.TYPE_STRING,
)

StoreDescriptionParameter = openapi.Schema(
    description='상점 설명',
    type=openapi.TYPE_STRING,
)

StoreRegisteredNumberParameter = openapi.Schema(
    description='상점 이름',
    type=openapi.TYPE_STRING
)

StoreLatParameter = openapi.Schema(
    description='상점 위치 정보',
    type=openapi.TYPE_NUMBER,
)

StoreLngParameter = openapi.Schema(
    description='상점 위치 정보',
    type=openapi.TYPE_NUMBER,
)

StoreInitBody = openapi.Schema(
    description='상점 생성 데이터',
    type=openapi.TYPE_OBJECT,
    properties={
        'name': StoreNameParameter,
        'description': StoreDescriptionParameter,
        'registered_number': StoreRegisteredNumberParameter,
        'lat': StoreLatParameter,
        'lng': StoreLngParameter,
    }
)

Lat = openapi.Parameter(
    'lat',
    openapi.IN_QUERY,
    description='상점 위치 정보',
    type=openapi.TYPE_NUMBER
)

Lng = openapi.Parameter(
    'lng',
    openapi.IN_QUERY,
    description='상점 위치 정보',
    type=openapi.TYPE_NUMBER
)

Distance = openapi.Parameter(
    'distance',
    openapi.IN_QUERY,
    description='검색 범위',
    type=openapi.TYPE_NUMBER
)