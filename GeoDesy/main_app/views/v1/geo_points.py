from rest_framework.response import Response
from main_app.serializers.v1 import geo_points

from main_app.views.base_view import BaseApiView

__all__ = (
    "GeoPointAPIView",
)


class GeoPointAPIView(BaseApiView):

    def post(self, request):
        serializer = geo_points.GeoPointSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.get_response())
