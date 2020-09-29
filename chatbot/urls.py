from django.urls import path

from chatbot import views

urlpatterns = [
    path("conversation/", views.get_conversation, name="get_conversation"),
    path("conversation/message/", views.post_message, name="post_message"),
]
