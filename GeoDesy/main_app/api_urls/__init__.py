from django.urls import path, include

urlpatterns = [
    path('v1/', include("main_app.api_urls.v1"))
]
