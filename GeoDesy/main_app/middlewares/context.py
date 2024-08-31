from utils.context import CurrentContext

__all__ = (
    "ContextMiddleware",
)


class ContextMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        ctx = CurrentContext()
        ctx.request = request
        response = self._get_response(request)
        ctx.clear()
        return response




