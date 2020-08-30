from drf_yasg import openapi

from account.documentation.models import SafeUser
from product.models import Category

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

Store = openapi.Schema(
    description='상점',
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(
            type=openapi.TYPE_INTEGER
        ),
        'name': StoreNameParameter,
        'registerer': openapi.Schema(
            description='관리자 목록',
            type=openapi.TYPE_ARRAY,
            items=SafeUser
        ),
        'description': StoreDescriptionParameter,
        'registered_number': StoreRegisteredNumberParameter,
        'location': openapi.Schema(
            type=openapi.TYPE_STRING
        )
    }
)

StoreInitBody = openapi.Schema(
    description='상점 생성 데이터',
    type=openapi.TYPE_OBJECT,
    properties={
        'name': StoreNameParameter,
        'register': openapi.Schema(
            description='관리자 목록',
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                description='사용자 ID',
                type=openapi.TYPE_INTEGER
            )
        ),
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

Ian = openapi.Schema(
    description='상품 바코드',
    type=openapi.TYPE_STRING
)

Price = openapi.Schema(
    description='상품 가격',
    type=openapi.TYPE_INTEGER
)

Amount = openapi.Schema(
    description='상품 수량',
    type=openapi.TYPE_INTEGER
)

ModifyStockBody = openapi.Schema(
    description='재고 수정 데이터',
    type=openapi.TYPE_OBJECT,
    properties={
        'ian': Ian,
        'price': Price,
        'amount': Amount
    }
)

Categories = openapi.Parameter(
    'category',
    openapi.IN_QUERY,
    description='상품 카테고리',
    type=openapi.TYPE_STRING,
    enum=[x[0] for x in Category.choices]
)

ProductName = openapi.Parameter(
    'name',
    openapi.IN_QUERY,
    description='상품 이름',
    type=openapi.TYPE_STRING
)

StockOrderByParameters = ['amount', 'id', 'price', 'product__name', 'product__ian', 'product__category']

StockOrderBy = openapi.Parameter(
    'order_by',
    openapi.IN_QUERY,
    description='정렬 기준',
    type=openapi.TYPE_STRING,
    enum=['amount', 'id', 'price', 'product__name', 'product__ian', 'product__category'] + ['-' + x for x in StockOrderByParameters]
)