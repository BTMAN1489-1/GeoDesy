from django.urls import path
from main_app.views.v1 import *

__all__ = ("urlpatterns",)

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view()),
    path('auth/', AuthorizationAPIView.as_view()),
    path('auth/change/', ChangeAuthAPIView.as_view()),
    path('auth/forgotten/password/', ForgottenPasswordView.as_view()),
    path('info/user/', UserInfoAPIView.as_view()),
    path('jwt/update/', UpdateJWTAPIView.as_view()),
    path('card/create/', CreateCardAPIView.as_view()),
    path('map/points/', GeoPointAPIView.as_view()),
    path('card/create/', CreateCardAPIView.as_view()),
    # path('card/update/', UpdateCardAPIView.as_view()),
    path('card/info/', ShowCardAPIView.as_view()),
    path('card/download/<uuid:card_uuid>/', DownloadCardPDF.as_view(), name="download_card"),
]
