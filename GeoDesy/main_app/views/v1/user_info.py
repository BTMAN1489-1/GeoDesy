from rest_framework.response import Response
from main_app.serializers.v1 import user_info
from main_app.views.v1.JWT import JWTAuthenticationAPIView

__all__ = (
    "UserInfoAPIView",
)


class UserInfoAPIView(JWTAuthenticationAPIView):

    def get(self, request):
        user = request.user
        return Response(user_info.UserInfoSerializer(user).data)

    def put(self, request):
        serializer = user_info.UserInfoSerializer(data=request.data, instance=request.user, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
