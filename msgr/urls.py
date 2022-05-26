
from django.urls import path
from django.views.generic import RedirectView

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
    path("chats/",
         RedirectView.as_view(pattern_name="msgr:main", permanent=True),
         name="chats"),
    path("chats/<int:pk>/",
         views.ChatView.as_view(),
         name="chat"),
    path("chats/<int:pk>/updates",
         views.ChatUpdatesView.as_view(),
         name="updates"),
    path("chats/delmessage/",
        views.ChatDeleteMessageView.as_view(),
        name="delete_message"),
]
