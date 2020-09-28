from django.urls import path

from chatbot import views

urlpatterns = [
    # path("", IsabotAppView.as_view(), name="home"),
    # path("api/isabot/", IsabotApiView.as_view(), name="isabot"),
    path("", views.get_conversation, name="get_conversation"),
    path(
        "conversation/",
        views.post_message,
        name="post_message",
    ),
]
