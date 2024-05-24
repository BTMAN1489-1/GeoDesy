from django.urls import path
from main_app.views.v1 import user_info, authorization, registration, JWT

urlpatterns = [
    path('registration/', registration.RegistrationAPIView.as_view()),
    path('auth/', authorization.AuthorizationAPIView.as_view()),
    path('auth/change/', authorization.ChangeAuthAPIView.as_view()),
    path('auth/forgotten/password/', authorization.ForgottenPasswordView.as_view()),
    path('info/user/', user_info.UserInfoAPIView.as_view()),
    path('jwt/update/', JWT.UpdateJWTAPIView.as_view()),
]
