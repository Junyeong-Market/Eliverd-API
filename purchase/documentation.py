from drf_yasg import openapi

from store.documentation import Lng, Lat

PgToken = openapi.Parameter(
    'KP Token',
    openapi.IN_QUERY,
    description='[KP] 카카오페이 거래 처리용 토큰',
    type=openapi.TYPE_STRING
)

Orders = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'store': openapi.Schema(
                '상점 PK',
                type=openapi.TYPE_INTEGER,
                description='상점 고유 키'
            ),
            'stocks': openapi.Schema(
                '재고 목록',
                type=openapi.TYPE_ARRAY,
                description='해당 상점에서 주문할 상품 목록',
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(
                            '재고 PK',
                            type=openapi.TYPE_INTEGER,
                            description='재고(Stock) 고유 키'
                        ),
                        "amount": openapi.Schema(
                            '수량',
                            type=openapi.TYPE_INTEGER,
                            description='주문 수량'
                        )
                    }
                )
            )
        }
    )
)

CreateOrderBody = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'orders': Orders,
        'deliver_to': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'lat': Lat,
                'lng': Lng
            }
        )
    }
)

KPNextRedirectURL = openapi.Schema(
    '카카오페이 리다이렉트 URL',
    type=openapi.TYPE_STRING,
    format=openapi.FORMAT_URI,
    description='카카오페이 결제로 리다이렉트 해주는 URL입니다.'
)

CreateOrderResponse = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'tid': openapi.Schema(
            '카카오페이 주문 고유 코드',
            type=openapi.TYPE_STRING,
            description='카카오페이에서 주문마다 부여하는 고유 코드입니다.',
        ),
        'oid': openapi.Schema(
            '주문 고유 코드',
            type=openapi.TYPE_INTEGER,
            description='Eliverd에서 주문마다 부여하는 고유 코드입니다.',
        ),
        'next_redirect_app_url': KPNextRedirectURL,
        'next_redirect_mobile_url': KPNextRedirectURL,
        'next_redirect_pc_url': KPNextRedirectURL,
        'android_app_scheme': KPNextRedirectURL,
        'ios_app_scheme': KPNextRedirectURL,
        'created_at': openapi.Schema(
            '주문 시간',
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_DATETIME,
            description='주문이 생성된 시간입니다.'
        ),
    }
)