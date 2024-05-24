from threading import Thread, active_count
from .algorithms import Singleton


class CustomThreadExecutor(Singleton):

    def __new__(cls, thread_name_prefix):
        obj = super().__new__(cls)
        obj._thread_name_prefix = "".join((thread_name_prefix, "-", str(active_count())))
        return obj

    def submit(self, __fn, is_daemon=True, *args, **kwargs):
        t = Thread(target=__fn, args=args, kwargs=kwargs, daemon=is_daemon, name=self._thread_name_prefix)
        t.start()
