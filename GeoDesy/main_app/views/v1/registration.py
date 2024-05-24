from rest_framework.response import Response
from rest_framework.views import APIView
from main_app.serializers.v1 import registration
from utils.context import CurrentContext, InContextAPI


class RegistrationAPIView(APIView):
    @InContextAPI()
    def post(self, request):
        serializer = registration.CreateRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = CurrentContext().response
        return Response(response)

    @InContextAPI()
    def put(self, request):
        serializer = registration.UpdateRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = CurrentContext().response
        return Response(response)
