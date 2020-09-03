from django.contrib import admin
from django.urls import path
from chatbot.views import ChatterBotAppView, ChatterBotApiView

urlpatterns = [
    path("", ChatterBotAppView.as_view(), name="main"),
    path("admin/", admin.site.urls),
    path("api/chatterbot/", ChatterBotApiView.as_view(), name="chatterbot"),
]
