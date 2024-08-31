from contextvars import ContextVar, copy_context
import enum
from functools import wraps
from utils.algorithms import Singleton
from utils.message_tools import EmailMessage

__all__ = (
    "TypeRequest", "ContextDescriptor", "CurrentContext", "set_api_context"
)


class TypeRequest(enum.Enum):
    API = enum.auto()
    SAME = enum.auto()


class ContextDescriptor:
    _var = None

    def __init__(self, default=None):
        self._default = default

    def __set_name__(self, owner, name):
        self._var = ContextVar(name, default=self._default)
        self.name = "_" + name

    def __set__(self, instance, value):
        self._var.set(value)

    def __get__(self, instance, owner):
        return self._var.get()

    def __delete__(self, instance):
        self._var.set(self._default)


class CurrentContext(Singleton):
    user = ContextDescriptor()
    type_request = ContextDescriptor(default=TypeRequest.SAME)
    request = ContextDescriptor()
    response = ContextDescriptor()
    message_handler = ContextDescriptor(default=EmailMessage)

    def clear(self):
        del self.response
        del self.request
        del self.type_request
        del self.user

    def copy_context(self):
        return copy_context()


def set_api_context(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ctx = CurrentContext()
        ctx.type_request = TypeRequest.API
        return func(*args, **kwargs)

    return wrapper


