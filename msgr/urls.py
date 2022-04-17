
from django.urls import path

from . import views


app_name = "msgr"

urlpatterns = [
    path("",
         views.ChatsListView.as_view(),
         name="main"),
    path("users/<int:pk>/",
         views.ProfilePageView.as_view(),
         name="profile_page"),
    path("chats/<int:pk>/",
         views.ChatView.as_view(),
         name="chat"),
]
