from rest_framework.response import Response
from main_app.serializers.v1 import geo_points
from rest_framework.views import APIView
from utils.context import InContextAPI


class GeoPointAPIView(APIView):

    @InContextAPI()
    def post(self, request):
        serializer = geo_points.GeoPointSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.get_response())
