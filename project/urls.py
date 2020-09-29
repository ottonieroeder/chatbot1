from chatbot import views
from django.conf.urls import handler404
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView

urlpatterns = [
    path("", views.IsabotAppView.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path("isabot/", include("chatbot.urls")),
    re_path(r"^(?P<path>.*)/$", views.IsabotAppView.as_view()),
]
