from rest_framework.response import Response
from rest_framework.views import APIView
from main_app.serializers.v1 import authorization
from utils.context import InContextAPI, CurrentContext
from .JWT import JWTAuthenticationAPIView


class AuthorizationAPIView(APIView):

    @InContextAPI()
    def post(self, request):
        serializer = authorization.CreateAuthorizationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        ctx = CurrentContext()
        return Response(ctx.response)


class ChangeAuthAPIView(JWTAuthenticationAPIView):

    @InContextAPI()
    def post(self, request):
        serializer = authorization.CreateChangeAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        ctx = CurrentContext()
        return Response(ctx.response)

    @InContextAPI()
    def put(self, request):
        serializer = authorization.UpdateChangeAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        ctx = CurrentContext()
        return Response(ctx.response)


class ForgottenPasswordView(APIView):

    @InContextAPI()
    def post(self, request):
        serializer = authorization.CreateForgottenPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        ctx = CurrentContext()
        return Response(ctx.response)

    @InContextAPI()
    def put(self, request):
        serializer = authorization.UpdateForgottenPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        ctx = CurrentContext()
        return Response(ctx.response)
