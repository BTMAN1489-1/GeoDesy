from rest_framework.exceptions import APIException
from django.core.exceptions import ValidationError as ModelValidationError
from rest_framework.exceptions import ValidationError as APIValidationError

__all__ = (
    "BadEnterAPIError", "NotFoundAPIError", "PermissionDeniedAPIError", "AuthenticationFailedAPIError",
    "FailedOperationAPIError", "ValidateError", "InvalidTokenError", "JsonSerializeError", "JsonDeserializeError"
)


class BadEnterAPIError(APIException):
    status_code = 400
    default_detail = 'Перепроверьте данные запроса.'
    default_code = 'bad_enter'


class NotFoundAPIError(APIException):
    status_code = 404
    default_detail = 'Запрашиваемые данные не были найдены'
    default_code = 'not_found'


class PermissionDeniedAPIError(APIException):
    status_code = 403
    default_detail = 'Вам отказано в доступе'
    default_code = 'permission_denied'


class AuthenticationFailedAPIError(APIException):
    status_code = 401
    default_detail = 'Неудачная попытка аутентификации'
    default_code = 'authentication_failed'


class FailedOperationAPIError(APIException):
    status_code = 406
    default_detail = "Ошибка при выполнении операции"
    default_code = 'failed_operation'


class ValidateError(Exception):

    def __new__(cls, msg):
        from utils.context import TypeRequest, CurrentContext

        type_request = CurrentContext().type_request
        if type_request == TypeRequest.API:
            return APIValidationError(msg)

        return ModelValidationError(msg)


class InvalidTokenError(Exception):
    """Класс исключения для невалидного токена"""


class JsonSerializeError(Exception):
    """Класс исключения для ошибок серилизации JSON оъектов"""


class JsonDeserializeError(Exception):
    """Класс исключения для ошибок десерилизации JSON оъектов"""
