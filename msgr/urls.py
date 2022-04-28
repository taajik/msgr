
from django.urls import path

from . import views


app_name = "msgr"

urlpatterns = [
    path("",
         views.ChatsListView.as_view(),
         name="main"),
    path("users/",
         views.SearchView.as_view(),
         name="search"),
    path("users/<int:pk>/",
         views.ProfilePageView.as_view(),
         name="profile"),
    path("chats/<int:pk>/",
         views.ChatView.as_view(),
         name="chat"),
]
