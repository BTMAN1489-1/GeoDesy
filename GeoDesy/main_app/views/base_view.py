from utils.context import set_api_context
from rest_framework.views import APIView

__all__ = ("BaseApiViewMeta", "BaseApiView")


class BaseApiViewMeta(type):
    _http_methods = ("post", "get", "put", "delete", "patch", "options", "head", "trace", "connect")

    def __new__(metacls, name, bases, spacename):
        methods = metacls._http_methods
        set_context = set_api_context
        for key, value in spacename.items():
            if callable(value) and key in methods:
                spacename[key] = set_context(value)
        return super().__new__(metacls, name, bases, spacename)


class BaseApiView(APIView, metaclass=BaseApiViewMeta):
    ...
