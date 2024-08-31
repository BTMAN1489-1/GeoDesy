from drf_spectacular.extensions import OpenApiViewExtension
from drf_spectacular.views import extend_schema
from drf_spectacular.utils import OpenApiExample
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from main_app.views.v1.JWT import JWTAuthenticationAPIView
from main_app.serializers.v1 import cards
from utils.upload_files.parsers import LimitedMultiPartParser

__all__ = (
    "DownloadCardPDFSchema", "CreateCardSchema", "ShowCardSchema", "UpdateCardSchema"
)


class CreateCardMock(JWTAuthenticationAPIView):
    parser_classes = (LimitedMultiPartParser, JSONParser)

    @extend_schema(
        tags=["Карточки ГГС"],
        summary="Создание карточки ГГС",
        examples=[OpenApiExample("Пример запроса", request_only=True, media_type="multipart/form-data",
                                 value=
                                 'outdoor_sign={"recommendation":"string","comment":"string","value":"saved"}\n'
                                 'type_of_sign={"recommendation":"string","comment":"string","value":"pyramid","properties":{"material":"wood","geometry":"tetrahedron"}}\n'
                                 'photos=@some_photo1.png;type=image/png\n'
                                 'photos=@some_photo2.png;type=image/png\n'
                                 'photos=@some_photo3.png;type=image/png\n'
                                 'monolith_two={"recommendation":"string","comment":"string","value":"covered"}\n'
                                 'sign_height_above_ground_level=-0.23\n'
                                 'sign_height=4.7\n'
                                 'federal_subject=Белгородская область\n'
                                 'latitude=90\n'
                                 'trench={"recommendation":"string","comment":"string","value":"readable"}\n'
                                 'longitude=180\n'
                                 'ORP_one={"recommendation":"string","comment":"string","value":"saved"}\n'
                                 'execute_date=2024-07-10\n'
                                 'monolith_three_and_four={"recommendation":"string","comment":"string","value":"covered"}\n'
                                 'ORP_two={"recommendation":"string","comment":"string","value":"saved"}\n'
                                 'monolith_one={"recommendation":"string","comment":"string","value":"saved"}\n'
                                 'identification_pillar={"recommendation":"string","comment":"string","value":"detected"}\n'
                                 'satellite_surveillance={"recommendation":"string","comment":"string","value":"possible"}'
                                 ),
                  OpenApiExample("Пирамида", request_only=True,
                                 description="""
<div>
<blockquote>
<ul>
<li>pyramid
<ul>
<li>properties
<ul>
<li>material (Возможные значения: metalic, wood)</li>
<li>geometry (Возможные значения: tetrahedron, trihedron)</li>
</ul>
</li>
</ul>
</li>
</ul>
</blockquote>
""",
                                 value={
                                     "value": "pyramid",
                                     "properties": {
                                         "material": "wood",
                                         "geometry": "trihedron"
                                     }
                                 }),
                  OpenApiExample("Сигнал", request_only=True,
                                 description="""
<div>
<blockquote>
<ul>
<li>signal
<ul>
<li>properties
<ul>
<li>type (Возможные значения: simple, complex)</li>
</ul>
</li>
</ul>
</li>
</ul>
</blockquote>
""",
                                 value={
                                     "value": "signal",
                                     "properties": {
                                         "type": "complex"
                                     }
                                 }),
                  OpenApiExample("Штатив", request_only=True,
                                 description="""
<div>
<blockquote>
<ul>
<li>tripod
<ul>
<li>properties
<ul>
<li>material (Возможные значения: metalic, wood)</li>
<li>geometry (Возможные значения: tetrahedron, trihedron)</li>
</ul>
</li>
</ul>
</li>
</ul>
</blockquote>
""",
                                 value={
                                     "value": "tripod",
                                     "properties": {
                                         "material": "metalic",
                                         "geometry": "tetrahedron"
                                     }
                                 }),
                  OpenApiExample("Тур", request_only=True,
                                 description="""
<div>
<blockquote>
<ul>
<li>tur
<ul>
<li>properties
<ul>
<li>pillar (Возможные значения: concrete, stone, brick)</li>
</ul>
</li>
</ul>
</li>
</ul>
</blockquote>
""",
                                 value={
                                     "value": "tur",
                                     "properties": {
                                         "pillar": "brick"
                                     }
                                 }),
                  OpenApiExample("Знак отсутствует", request_only=True,
                                 description="""
<div>
<blockquote>
<ul>
<li>no_sign
</li>
</ul>
</blockquote>
""",
                                 value={
                                     "value": "no_sign"
                                 }),
                  ],

        request=cards.CreateCardForUserSerializer,
        responses=None
    )
    def post(self, request):
        ...


class ShowCardMock(JWTAuthenticationAPIView):

    @extend_schema(
        tags=["Карточки ГГС"],
        summary="Информация о карточках ГГС",
        request=cards.ShowCardSerializer,
        responses={status.HTTP_200_OK: cards.ShowCardSerializer(many=True)}
    )
    def post(self, request):
        ...


class DownloadCardPDFMock(APIView):

    @extend_schema(
        tags=["Карточки ГГС"],
        summary="Загрузка PDF"
    )
    def get(self, request):
        ...


class UpdateCardMock(JWTAuthenticationAPIView):
    @extend_schema(
        tags=["Карточки ГГС"],
        summary="Обновление информации о карточке ГГС",
        request=cards.UpdateCardForStuffSerializer,
        responses=None
    )
    def post(self, request):
        ...


class DownloadCardPDFSchema(OpenApiViewExtension):
    target_class = 'main_app.views.v1.cards.DownloadCardPDF'

    def view_replacement(self):
        return DownloadCardPDFMock


class CreateCardSchema(OpenApiViewExtension):
    target_class = 'main_app.views.v1.cards.CreateCardAPIView'

    def view_replacement(self):
        return CreateCardMock


class ShowCardSchema(OpenApiViewExtension):
    target_class = 'main_app.views.v1.cards.ShowCardAPIView'

    def view_replacement(self):
        return ShowCardMock


class UpdateCardSchema(OpenApiViewExtension):
    target_class = 'main_app.views.v1.cards.UpdateCardAPIView'

    def view_replacement(self):
        return UpdateCardMock
