from chatbot import views
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView

urlpatterns = [
    path("", views.IsabotAppView.as_view(), name="home"),
    re_path(r"^favicon\.ico$", RedirectView.as_view(url="/static/img/favicon.ico")),
    path("admin/", admin.site.urls),
    path("isabot/", include("chatbot.urls")),
]
