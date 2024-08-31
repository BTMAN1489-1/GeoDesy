from rest_framework.response import Response
from main_app.serializers.v1 import authorization
from utils.context import CurrentContext
from main_app.views.v1.JWT import JWTAuthenticationAPIView
from main_app.views.base_view import BaseApiView
__all__ = (
    "AuthorizationAPIView", "ChangeAuthAPIView", "ForgottenPasswordView"
)


class AuthorizationAPIView(BaseApiView):

    def post(self, request):
        serializer = authorization.CreateAuthorizationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        ctx = CurrentContext()
        return Response(ctx.response)


class ChangeAuthAPIView(JWTAuthenticationAPIView):

    def post(self, request):
        serializer = authorization.CreateChangeAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        ctx = CurrentContext()
        return Response(ctx.response)

    def put(self, request):
        serializer = authorization.UpdateChangeAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response()


class ForgottenPasswordView(BaseApiView):

    def post(self, request):
        serializer = authorization.CreateForgottenPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        ctx = CurrentContext()
        return Response(ctx.response)

    def put(self, request):
        serializer = authorization.UpdateForgottenPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response()
