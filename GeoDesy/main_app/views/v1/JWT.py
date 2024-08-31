from rest_framework.response import Response
from main_app.serializers.v1 import authorization
from main_app.auth import JWTAuthentication
from main_app.views.base_view import BaseApiView
from utils.context import CurrentContext


__all__ = (
    "JWTAuthenticationAPIView", "UpdateJWTAPIView"
)


class JWTAuthenticationAPIView(BaseApiView):
    authentication_classes = (JWTAuthentication,)


class UpdateJWTAPIView(BaseApiView):

    def post(self, request):
        serializer = authorization.UpdateJWTSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(CurrentContext().response)
