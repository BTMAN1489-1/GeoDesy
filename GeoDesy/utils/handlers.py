from utils.algorithms import Singleton
from utils.message_tools import EmailMessage, Message
from utils.threads import CustomThreadExecutor

__all__ = (
    "MessageHandler"
)


class MessageHandler(Singleton):
    _message_class = EmailMessage

    def __new__(cls, user, *args, **kwargs):
        obj = super().__new__(cls)
        obj.user = user
        return obj

    def send_confirm_code(self, confirm_code, message_class=object):
        if issubclass(message_class, Message):
            message = message_class(self.user)
        else:
            message = self._message_class(self.user)

        message.init_confirm_code(confirm_code)
        _executor = CustomThreadExecutor(thread_name_prefix=self.__class__.__name__)
        _executor.submit(message.send)

