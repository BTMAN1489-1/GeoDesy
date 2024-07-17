from drf_spectacular.extensions import OpenApiViewExtension
from drf_spectacular.views import extend_schema
from rest_framework import status, serializers
from main_app.views.v1 import JWT
from main_app.serializers.v1 import geo_points


class GeoPointResponse(serializers.Serializer):
    latitude = serializers.FloatField(min_value=-90, max_value=90)
    longitude = serializers.FloatField(min_value=-180, max_value=180)
    guid = serializers.UUIDField()


class GeoPointMock(JWT.APIView):
    @extend_schema(
        tags=["Карта"],
        summary="Получение списка координат пунктов ГГС",
        request=geo_points.GeoPointSerializer,
        responses={status.HTTP_200_OK: GeoPointResponse(many=True)}
    )
    def post(self, request):
        ...


class GeoPointSchema(OpenApiViewExtension):
    target_class = 'main_app.views.v1.geo_points.GeoPointAPIView'

    def view_replacement(self):
        return GeoPointMock
