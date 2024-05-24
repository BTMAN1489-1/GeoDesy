from rest_framework.response import Response
from rest_framework.views import APIView
from main_app.serializers.v1 import authorization
from main_app.auth import JWTAuthentication
from utils.context import InContextAPI, CurrentContext


class JWTAuthenticationAPIView(APIView):
    authentication_classes = (JWTAuthentication,)


class UpdateJWTAPIView(APIView):

    @InContextAPI()
    def post(self, request):
        serializer = authorization.UpdateJWTSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(CurrentContext().response)
