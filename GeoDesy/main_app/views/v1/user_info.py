from rest_framework.response import Response
from main_app.serializers.v1 import user_info
from .JWT import JWTAuthenticationAPIView
from utils.context import InContextAPI


class UserInfoAPIView(JWTAuthenticationAPIView):

    @InContextAPI()
    def get(self, request):
        user = request.user
        return Response(user_info.UserInfoSerializer(user).data)

    @InContextAPI()
    def put(self, request):
        serializer = user_info.UserInfoSerializer(data=request.data, instance=request.user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
