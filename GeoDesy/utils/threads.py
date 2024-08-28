from threading import Thread, active_count
from .algorithms import Singleton
from contextvars import ContextVar


class CustomThreadExecutor(Singleton):
    _thread_name_prefix = ContextVar("thread_name_prefix")

    def __new__(cls, thread_name_prefix):
        obj = super().__new__(cls)
        cls._thread_name_prefix.set("".join((thread_name_prefix, "-", str(active_count()))))
        return obj

    def submit(self, __fn, is_daemon=True, *args, **kwargs):
        t = Thread(target=__fn, args=args, kwargs=kwargs, daemon=is_daemon, name=self._thread_name_prefix.get())
        t.start()
