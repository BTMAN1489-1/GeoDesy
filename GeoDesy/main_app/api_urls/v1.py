from django.urls import path
from main_app.views.v1 import user_info, authorization, registration, JWT, cards, geo_points

urlpatterns = [
    path('registration/', registration.RegistrationAPIView.as_view()),
    path('auth/', authorization.AuthorizationAPIView.as_view()),
    path('auth/change/', authorization.ChangeAuthAPIView.as_view()),
    path('auth/forgotten/password/', authorization.ForgottenPasswordView.as_view()),
    path('info/user/', user_info.UserInfoAPIView.as_view()),
    path('jwt/update/', JWT.UpdateJWTAPIView.as_view()),
    path('card/create/', cards.CreateCardAPIView.as_view()),
    path('map/points/', geo_points.GeoPointAPIView.as_view()),
    path('card/create/', cards.CreateCardAPIView.as_view()),
    path('card/update/', cards.UpdateCardAPIView.as_view()),
    path('card/info/', cards.ShowCardAPIView.as_view()),
]
