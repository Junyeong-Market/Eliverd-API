from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.parsers import FileUploadParser

from assets.models import Asset
from assets.serializers import AssetSerializer


class FileUploadAPI(CreateAPIView):
    serializer_class = AssetSerializer
    parser_classes = [FileUploadParser]

    @swagger_auto_schema(operation_summary='파일 업로드',
                         operation_description='파일을 AWS S3로 업로드합니다. Content-Type는 파일 MIME을 사용합니다. '
                                               'Content-Disposition 헤더로 `Content-Disposition:inline;filename=(파일 '
                                               '이름)`을 포함합니다.')
    def post(self, request, *args, **kwargs):
        request.data['image'] = request.data['file']
        return super().post(request, *args, **kwargs)


class GetAssetAPI(RetrieveAPIView):
    serializer_class = AssetSerializer

    @swagger_auto_schema(operation_summary='파일 조회', operation_description='파일을 조회합니다.')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        return Asset.objects.get(id=self.kwargs['id'])
