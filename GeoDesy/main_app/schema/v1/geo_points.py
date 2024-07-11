from drf_spectacular.extensions import OpenApiViewExtension
from drf_spectacular.views import extend_schema
from rest_framework import status
from main_app.views.v1 import JWT
from main_app.serializers.v1 import geo_points


class GeoPointMock(JWT.APIView):
    @extend_schema(
        tags=["Карта"],
        summary="Получение списка координат пунктов ГГС",
        request=geo_points.GeoPointSerializer,
        responses={status.HTTP_200_OK: geo_points.GeoPointSerializer(many=True)}
    )
    def post(self, request):
        ...


class GeoPointSchema(OpenApiViewExtension):
    target_class = 'main_app.views.v1.map.GeoPointAPIView'

    def view_replacement(self):
        return GeoPointMock
