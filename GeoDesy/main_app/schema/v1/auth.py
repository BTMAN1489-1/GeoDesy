from drf_spectacular.extensions import OpenApiAuthenticationExtension, OpenApiViewExtension
from drf_spectacular.views import extend_schema
from drf_spectacular.utils import OpenApiTypes, OpenApiExample, OpenApiParameter, OpenApiResponse, extend_schema_view
from rest_framework import status
from main_app.views.v1 import JWT
from main_app.schema import utils
from main_app.serializers.v1 import TFA, authorization


class JWTAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'main_app.auth.JWTAuthentication'  # full import path OR class ref
    name = 'JWTAuthentication'  # name used in the schema

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'header',
            'name': "Authorization",
        }


class AuthorizationMock(JWT.APIView):

    @extend_schema(
        tags=["Авторизация"],
        summary="Вход по паролю",

        auth=None,
        examples=[OpenApiExample("Пример запроса 1", request_only=True,
                                 value={
                                     "email": "12345@yandex.ru",
                                     "password": "12345"
                                 }),
                  OpenApiExample("Пример ответа 1", response_only=True, status_codes=[status.HTTP_200_OK, ],
                                 value={
                                     "access_token": "65794a68624763694f694a435445464c5256387951694973496e5631615751694f6949774d6d56694d7a56684e4451325a474d305957466b59544a684e6a457a4f4445335954597a4f574a6d5a434973496e5235634755694f694a6859324e6c63334d694c434a7a59577830496a6f69597a42694d544268596a55314e3251784e7a4979597a63354d6a426d4d7a426c4e4441784d44497a4f546b694c434a6c65484270636d46306157397558325268644756306157316c496a6f694d6a41794e4330774e7930774d5651784e446f774e446f784e6934774d7a51344f444d6966513d3d.3c6204cb452b8c681935541ac75a3d4a457d5065c7282bd87cbcc95135f67b6d2d021e5876689aafe6a0d3917d95689d38651af578e243e87d42b7e967e2102a",
                                     "refresh_token": "65794a68624763694f694a435445464c5256387951694973496e5631615751694f6949774d6d56694d7a56684e4451325a474d305957466b59544a684e6a457a4f4445335954597a4f574a6d5a434973496e5235634755694f694a6859324e6c63334d694c434a7a59577830496a6f69597a42694d544268596a55314e3251784e7a4979597a63354d6a426d4d7a426c4e4441784d44497a4f546b694c434a6c65484270636d46306157397558325268644756306157316c496a6f694d6a41794e4330774e7930774d5651784e446f774e446f784e6934774d7a51344f444d6966513d3d.3c6204cb452b8c681935541ac75a3d4a457d5065c7282bd87cbcc95135f67b6d2d021e5876689aafe6a0d3917d95689d38651af578e243e87d42b7e967e2102a",
                                     "expiration_access_token_in_seconds": 18000
                                 }),
                  ],
        request=authorization.CreateAuthorizationSerializer,
        responses={status.HTTP_200_OK: utils.JWTSuccessResponse}
    )
    def post(self, request):
        ...


class ChangeAuthMock(JWT.JWTAuthenticationAPIView):

    @extend_schema(
        tags=["Авторизация"],
        description="""
<pre>
Изменение данных аутентификации пользователя, ровно как и регистрация, происходит в два этапа:
<br />\t1.1) Mетод POST, в случае успеха, передает в ответе TFA-токен
<br />\t1.2) Пользователю на указанную почту приходит код подтверждения
<br />\t2) Клиент должен вызвать метод PUT, передав в тело запроса TFA-токен и код подтверждения
</pre>
""",
        summary="Изменение данных аутентификации. Первый этап",

        examples=[
            OpenApiExample("Пример запроса 1", request_only=True,
                           description="В запросе можно указать новый пароль и e-mail.",
                           value={
                               "email": "12345@gmail.com",
                               "password": "qwerty"
                           }),
            OpenApiExample("Пример запроса 2", request_only=True,
                           description="В запросе можно указать только новый пароль.",
                           value={
                               "password": "qwerty"
                           }),
            OpenApiExample("Пример запроса 3", request_only=True,
                           description="В запросе можно указать только новый e-mail.",
                           value={
                               "email": "12345@gmail.com"
                           }),
            OpenApiExample("Пример ответа", response_only=True, status_codes=[status.HTTP_200_OK, ],
                           value={
                               "tfa_token": "65794a3164576c6b496a6f69597a49794f5463314e5755344e7a68684e445669597a67324e4751344e4752694d446c6c5a5446684f446b694c434a6c646d567564434936496c4a6c5a326c7a64484a6864476c7662694973496d567459576c73496a6f694d54497a4e445641655746755a4756344c6e4a31496977696347467a63336476636d52666147467a61434936496e42696132526d4d6c397a614745794e54596b4e7a49774d4441774a485a4b5430464d516b703559586c34635867334e45744863304a4353336b6b57565647596c4e4859577333616e4e71515774306148424a6447396e51553134643164485757526c5a5778634c304a725457526a5a7a644c55306b39496977695a6d6c7963335266626d46745a534936496c78314d4451784e4678314d44517a4d4678314d44517a4e3178314d44517a4e4678314d4451304d4678314d44517a4d4678314d44517a5a6c78314d44517a4e5678314d4451304d4678314d44517a593178314d44517a4d434973496e4e6c593239755a4639755957316c496a6f69584855774e444930584855774e444d34584855774e444e69584855774e444d77584855774e445179584855774e444e6c584855774e444d794969776964476870636d5266626d46745a534936496c78314d4451795a6c78314d44517a5a4678314d445130596c78314d4451304e794973496e4e6c65434936496d31686247556966513d3d.95680e5cff0bdf80d586e26d2da34460ea4dc18ce173af977ac1043f579acc551014df279adcd7bfaef36d3d1ad4e508f3010168ae9d7d3df9e282c11560c951",
                               "expiration_confirm_code_in_seconds": 200
                           }),
        ],
        request=authorization.CreateChangeAuthSerializer,
        responses={status.HTTP_200_OK: TFA.TwoFactoryAuthentication}
    )
    def post(self, request):
        ...

    @extend_schema(
        tags=["Авторизация"],
        summary="Изменение данных аутентификации. Второй этап",
        examples=[OpenApiExample("Запрос", request_only=True,
                                 value={
                                     "tfa_token": "65794a3164576c6b496a6f69597a49794f5463314e5755344e7a68684e445669597a67324e4751344e4752694d446c6c5a5446684f446b694c434a6c646d567564434936496c4a6c5a326c7a64484a6864476c7662694973496d567459576c73496a6f694d54497a4e445641655746755a4756344c6e4a31496977696347467a63336476636d52666147467a61434936496e42696132526d4d6c397a614745794e54596b4e7a49774d4441774a485a4b5430464d516b703559586c34635867334e45744863304a4353336b6b57565647596c4e4859577333616e4e71515774306148424a6447396e51553134643164485757526c5a5778634c304a725457526a5a7a644c55306b39496977695a6d6c7963335266626d46745a534936496c78314d4451784e4678314d44517a4d4678314d44517a4e3178314d44517a4e4678314d4451304d4678314d44517a4d4678314d44517a5a6c78314d44517a4e5678314d4451304d4678314d44517a593178314d44517a4d434973496e4e6c593239755a4639755957316c496a6f69584855774e444930584855774e444d34584855774e444e69584855774e444d77584855774e445179584855774e444e6c584855774e444d794969776964476870636d5266626d46745a534936496c78314d4451795a6c78314d44517a5a4678314d445130596c78314d4451304e794973496e4e6c65434936496d31686247556966513d3d.95680e5cff0bdf80d586e26d2da34460ea4dc18ce173af977ac1043f579acc551014df279adcd7bfaef36d3d1ad4e508f3010168ae9d7d3df9e282c11560c951",
                                     "confirm_code": "654321"}),
                  ],
        request=authorization.UpdateChangeAuthSerializer,
        responses=None
    )
    def put(self, request):
        ...


class ForgottenPasswordMock(JWT.APIView):

    @extend_schema(
        tags=["Авторизация"],
        description="""
<pre>
Аналогично изменению данных аутентификации пользователя и регистрации.
</pre>
""",
        summary="Забыли пароль, сэр? Ну что ж бывает. Первый этап",

        examples=[
            OpenApiExample("Пример запроса 1", request_only=True,
                           description="В запросе необходимо указать e-mail и новый пароль.",
                           value={
                               "email": "12345@gmail.com",
                               "password": "qwerty"
                           }),
            OpenApiExample("Пример ответа", response_only=True, status_codes=[status.HTTP_200_OK, ],
                           value={
                               "tfa_token": "65794a3164576c6b496a6f69597a49794f5463314e5755344e7a68684e445669597a67324e4751344e4752694d446c6c5a5446684f446b694c434a6c646d567564434936496c4a6c5a326c7a64484a6864476c7662694973496d567459576c73496a6f694d54497a4e445641655746755a4756344c6e4a31496977696347467a63336476636d52666147467a61434936496e42696132526d4d6c397a614745794e54596b4e7a49774d4441774a485a4b5430464d516b703559586c34635867334e45744863304a4353336b6b57565647596c4e4859577333616e4e71515774306148424a6447396e51553134643164485757526c5a5778634c304a725457526a5a7a644c55306b39496977695a6d6c7963335266626d46745a534936496c78314d4451784e4678314d44517a4d4678314d44517a4e3178314d44517a4e4678314d4451304d4678314d44517a4d4678314d44517a5a6c78314d44517a4e5678314d4451304d4678314d44517a593178314d44517a4d434973496e4e6c593239755a4639755957316c496a6f69584855774e444930584855774e444d34584855774e444e69584855774e444d77584855774e445179584855774e444e6c584855774e444d794969776964476870636d5266626d46745a534936496c78314d4451795a6c78314d44517a5a4678314d445130596c78314d4451304e794973496e4e6c65434936496d31686247556966513d3d.95680e5cff0bdf80d586e26d2da34460ea4dc18ce173af977ac1043f579acc551014df279adcd7bfaef36d3d1ad4e508f3010168ae9d7d3df9e282c11560c951",
                               "expiration_confirm_code_in_seconds": 200
                           }),
        ],
        request=authorization.CreateForgottenPasswordSerializer,
        responses={status.HTTP_200_OK: TFA.TwoFactoryAuthentication}
    )
    def post(self, request):
        ...

    @extend_schema(
        tags=["Авторизация"],
        summary="Забыли пароль, сэр? Ну что ж бывает. Второй этап",
        examples=[OpenApiExample("Запрос", request_only=True,
                                 value={
                                     "tfa_token": "65794a3164576c6b496a6f69597a49794f5463314e5755344e7a68684e445669597a67324e4751344e4752694d446c6c5a5446684f446b694c434a6c646d567564434936496c4a6c5a326c7a64484a6864476c7662694973496d567459576c73496a6f694d54497a4e445641655746755a4756344c6e4a31496977696347467a63336476636d52666147467a61434936496e42696132526d4d6c397a614745794e54596b4e7a49774d4441774a485a4b5430464d516b703559586c34635867334e45744863304a4353336b6b57565647596c4e4859577333616e4e71515774306148424a6447396e51553134643164485757526c5a5778634c304a725457526a5a7a644c55306b39496977695a6d6c7963335266626d46745a534936496c78314d4451784e4678314d44517a4d4678314d44517a4e3178314d44517a4e4678314d4451304d4678314d44517a4d4678314d44517a5a6c78314d44517a4e5678314d4451304d4678314d44517a593178314d44517a4d434973496e4e6c593239755a4639755957316c496a6f69584855774e444930584855774e444d34584855774e444e69584855774e444d77584855774e445179584855774e444e6c584855774e444d794969776964476870636d5266626d46745a534936496c78314d4451795a6c78314d44517a5a4678314d445130596c78314d4451304e794973496e4e6c65434936496d31686247556966513d3d.95680e5cff0bdf80d586e26d2da34460ea4dc18ce173af977ac1043f579acc551014df279adcd7bfaef36d3d1ad4e508f3010168ae9d7d3df9e282c11560c951",
                                     "confirm_code": "654321"}),
                  ],
        request=authorization.UpdateForgottenPasswordSerializer,
        responses=None
    )
    def put(self, request):
        ...


class UpdateJWTMock(JWT.APIView):

    @extend_schema(
        tags=["Авторизация"],
        summary="Обновление JWT-токена",

        examples=[
            OpenApiExample("Пример запроса 1", request_only=True,
                           value={
                               "refresh_token": "65794a68624763694f694a435445464c5256387951694973496e5631615751694f6949774d6d56694d7a56684e4451325a474d305957466b59544a684e6a457a4f4445335954597a4f574a6d5a434973496e5235634755694f694a6859324e6c63334d694c434a7a59577830496a6f69597a42694d544268596a55314e3251784e7a4979597a63354d6a426d4d7a426c4e4441784d44497a4f546b694c434a6c65484270636d46306157397558325268644756306157316c496a6f694d6a41794e4330774e7930774d5651784e446f774e446f784e6934774d7a51344f444d6966513d3d.3c6204cb452b8c681935541ac75a3d4a457d5065c7282bd87cbcc95135f67b6d2d021e5876689aafe6a0d3917d95689d38651af578e243e87d42b7e967e2102a"
                           }),
            OpenApiExample("Пример ответа", response_only=True, status_codes=[status.HTTP_200_OK, ],
                           value={
                               "access_token": "65794a68624763694f694a435445464c5256387951694973496e5631615751694f6949774d6d56694d7a56684e4451325a474d305957466b59544a684e6a457a4f4445335954597a4f574a6d5a434973496e5235634755694f694a6859324e6c63334d694c434a7a59577830496a6f69597a42694d544268596a55314e3251784e7a4979597a63354d6a426d4d7a426c4e4441784d44497a4f546b694c434a6c65484270636d46306157397558325268644756306157316c496a6f694d6a41794e4330774e7930774d5651784e446f774e446f784e6934774d7a51344f444d6966513d3d.3c6204cb452b8c681935541ac75a3d4a457d5065c7282bd87cbcc95135f67b6d2d021e5876689aafe6a0d3917d95689d38651af578e243e87d42b7e967e2102a",
                               "refresh_token": "65794a68624763694f694a435445464c5256387951694973496e5631615751694f6949774d6d56694d7a56684e4451325a474d305957466b59544a684e6a457a4f4445335954597a4f574a6d5a434973496e5235634755694f694a6859324e6c63334d694c434a7a59577830496a6f69597a42694d544268596a55314e3251784e7a4979597a63354d6a426d4d7a426c4e4441784d44497a4f546b694c434a6c65484270636d46306157397558325268644756306157316c496a6f694d6a41794e4330774e7930774d5651784e446f774e446f784e6934774d7a51344f444d6966513d3d.3c6204cb452b8c681935541ac75a3d4a457d5065c7282bd87cbcc95135f67b6d2d021e5876689aafe6a0d3917d95689d38651af578e243e87d42b7e967e2102a",
                               "expiration_access_token_in_seconds": 18000
                           }),
        ],
        request=authorization.UpdateJWTSerializer,
        responses={status.HTTP_200_OK: utils.JWTSuccessResponse}
    )
    def post(self, request):
        ...


class AuthorizationSchema(OpenApiViewExtension):
    target_class = 'main_app.views.v1.authorization.AuthorizationAPIView'

    def view_replacement(self):
        return AuthorizationMock


class ChangeAuthSchema(OpenApiViewExtension):
    target_class = 'main_app.views.v1.authorization.ChangeAuthAPIView'

    def view_replacement(self):
        return ChangeAuthMock


class ForgottenPasswordSchema(OpenApiViewExtension):
    target_class = 'main_app.views.v1.authorization.ForgottenPasswordView'

    def view_replacement(self):
        return ForgottenPasswordMock


class UpdateJWTSchema(OpenApiViewExtension):
    target_class = 'main_app.views.v1.JWT.UpdateJWTAPIView'

    def view_replacement(self):
        return UpdateJWTMock
