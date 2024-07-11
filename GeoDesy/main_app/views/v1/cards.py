from rest_framework.response import Response
from main_app.serializers.v1 import cards
from main_app.permissions import StaffOnlyPermission
from .JWT import JWTAuthenticationAPIView
from utils.context import InContextAPI, CurrentContext
from utils.upload_files.parsers import LimitedMultiPartParser
from rest_framework.parsers import JSONParser


class CreateCardAPIView(JWTAuthenticationAPIView):
    parser_classes = (LimitedMultiPartParser,)

    @InContextAPI()
    def post(self, request):
        ctx = CurrentContext()
        user = ctx.user
        if user.is_staff:
            serializer = cards.CreateCardForStuffSerializer(data=request.data)
        else:
            serializer = cards.CreateCardForUserSerializer(data=request.data)
        # raise serializer.errors
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response()


class UpdateCardAPIView(JWTAuthenticationAPIView):
    permission_classes = (StaffOnlyPermission,)

    @InContextAPI()
    def post(self, request):
        serializer = cards.UpdateCardForStuffSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response()


class ShowCardAPIView(JWTAuthenticationAPIView):

    @InContextAPI()
    def post(self, request):
        serializer = cards.ShowCardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        ctx = CurrentContext()
        return Response(ctx.response)
