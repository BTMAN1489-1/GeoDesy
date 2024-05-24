from datetime import datetime
from rest_framework import authentication
from utils.auth_tools import parse_jwt_token, TypeToken
from utils.algorithms import deserialize_to_dict
from main_app.models import Session
from main_app.exceptions import InvalidTokenError, AuthenticationFailedAPIError
from utils.context import CurrentContext


class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        jwt_token = request.META.get('HTTP_AUTHORIZATION', None)
        msg = "В доступе отказано."
        try:
            binary_data, jwt_sign = parse_jwt_token(jwt_token)
            data = deserialize_to_dict(binary_data)

            if data['type'] == TypeToken.ACCESS:
                current_datetime = datetime.utcnow()
                expiration_datetime = data["expiration_datetime"]
                expiration_datetime = datetime.fromisoformat(expiration_datetime)

                # if current_datetime <= expiration_datetime:
                session = Session.objects.get(api_id=data['uuid'])
                ctx = CurrentContext()
                ctx.user = session.user

                return ctx.user, session

            raise InvalidTokenError()

        except Exception:
            raise AuthenticationFailedAPIError(msg)


