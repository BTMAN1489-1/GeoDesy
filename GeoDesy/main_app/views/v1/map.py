from rest_framework.response import Response
from main_app.serializers.v1 import map
from rest_framework.views import APIView
from utils.context import InContextAPI


class GeoPointAPIView(APIView):

    @InContextAPI()
    def post(self, request):
        serializer = map.GeoPointSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.get_response())
