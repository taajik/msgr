
from django.urls import path

from . import views


app_name = "msgr"

urlpatterns = [
    path("users/<int:pk>/",
         views.ProfilePageView.as_view(),
         name="profile_page"),
]
