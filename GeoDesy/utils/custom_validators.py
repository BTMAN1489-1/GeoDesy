from main_app.exceptions import ValidateError, InvalidTokenError, BadEnterAPIError
from main_app import models
from utils.auth_tools import parse_token, verify_token


def validate_russian_text(russian_text: str):
    allow_letters = set('ЙЦУКЕНГШЩЗХФЫВАПРОЛДЖЭЯЧСМИТБЮЁёйцукенгшщзхъфывапролджэячсмитбюь')
    if not set(russian_text).issubset(allow_letters):
        raise ValidateError("Ипользуйте только символы русского (православного) алфавита")


def validate_token(token: str):
    try:
        binary_data, sign = parse_token(token)
        has_verified = verify_token(binary_data, sign)

        if not has_verified:
            raise InvalidTokenError()

    except InvalidTokenError:

        raise ValidateError("Недействительный токен.")

    return binary_data


def check_unique_email(email):
    has_login = models.User.objects.filter(email=email).exists()
    if has_login:
        raise BadEnterAPIError(f"Email {email} уже занат.")

