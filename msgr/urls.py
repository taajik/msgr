
from django.urls import path

from . import views


app_name = "msgr"

urlpatterns = [
    path("",
         views.ChatsView.as_view(),
         name="main"),
    path("users/<int:pk>/",
         views.ProfilePageView.as_view(),
         name="profile_page"),
]
