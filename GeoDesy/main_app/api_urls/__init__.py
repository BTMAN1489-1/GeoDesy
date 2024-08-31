from django.urls import path, include

__all__ = ("urlpatterns",)

urlpatterns = [
    path('v1/', include("main_app.api_urls.v1"))
]
