from django.contrib import admin
from django.urls import path
from chatbot.views import IsabotAppView, IsabotApiView

urlpatterns = [
    path("", IsabotAppView.as_view(), name="main"),
    path("admin/", admin.site.urls),
    path("api/isabot/", IsabotApiView.as_view(), name="isabot"),
]
