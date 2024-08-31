from rest_framework.response import Response
from main_app.serializers.v1 import registration
from main_app.views.base_view import BaseApiView
from utils.context import CurrentContext

__all__ = (
    "RegistrationAPIView",
)


class RegistrationAPIView(BaseApiView):
    def post(self, request):
        ctx = CurrentContext()
        serializer = registration.CreateRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = ctx.response
        return Response(response)

    def put(self, request):
        ctx = CurrentContext()
        serializer = registration.UpdateRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = ctx.response
        return Response(response)
