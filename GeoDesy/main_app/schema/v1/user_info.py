from drf_spectacular.extensions import OpenApiViewExtension
from drf_spectacular.views import extend_schema
from drf_spectacular.utils import OpenApiExample
from rest_framework import status
from main_app.views.v1.JWT import JWTAuthenticationAPIView
from main_app.serializers.v1 import user_info

__all__ = (
    "UserInfoSchema",
)


class UserInfoMock(JWTAuthenticationAPIView):
    @extend_schema(
        tags=["О пользователе"],
        summary="Получение информации о пользователе",
        examples=[OpenApiExample("Запрос", request_only=True,
                                 value={"first_name": "Даздраперма", "second_name": "Филатов", "third_name": "Яныч",
                                        "sex": "male",
                                        "email": "12345@yandex.ru",
                                        "password": "12345"})],
        request=user_info.UserInfoSerializer,
        responses={status.HTTP_200_OK: user_info.UserInfoSerializer}
    )
    def get(self, request):
        ...

    @extend_schema(
        tags=["О пользователе"],
        summary="Изменение информации о пользователе",
        description="""
<pre>
Допускаетя частичное изменение информации о пользователе. Т.е. в теле запроса необязательно указывать все поля.
</pre>
""",
        examples=[OpenApiExample("Полное обновление", request_only=True,
                                 value={
                                     "first_name": "Василий", "second_name": "Ульянов", "third_name": "Ильич",
                                     "sex": "unknown"
                                 }),
                  OpenApiExample("Частичное обновление", request_only=True,
                                 value={"first_name": "Василий",
                                        "sex": "unknown"})],
        request=user_info.UserInfoSerializer,
        responses={status.HTTP_200_OK: user_info.UserInfoSerializer}
    )
    def put(self, request):
        ...


class UserInfoSchema(OpenApiViewExtension):
    target_class = 'main_app.views.v1.user_info.UserInfoAPIView'

    def view_replacement(self):
        return UserInfoMock
