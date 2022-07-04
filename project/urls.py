"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.generic import TemplateView

from accounts import views as account_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("",
         TemplateView.as_view(template_name="home.html"),
         name="home"),

    path("signup/",
         account_views.SignupView.as_view(),
         name="signup"),
    path("login/",
         auth_views.LoginView.as_view(next_page="profile"),
         name="login"),
    path("logout/",
         auth_views.LogoutView.as_view(next_page="home"),
         name="logout"),
    path("profile/",
         account_views.ProfileView.as_view(),
         name="profile"),

    path("password_reset/",
         auth_views.PasswordResetView.as_view(),
         name="password_reset"),
    path("password_reset/done/",
         auth_views.PasswordResetDoneView.as_view(),
         name="password_reset_done"),
    path("reset/<uidb64>/<token>/",
         auth_views.PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
    path("reset/done/",
         auth_views.PasswordResetCompleteView.as_view(),
         name="password_reset_complete"),
    # path("password_change/",
    #      auth_views.PasswordChangeView.as_view(),
    #      name="password_change"),
    # path("password_change/done/",
    #      auth_views.PasswordChangeDoneView.as_view(),
    #      name="password_change_done"),

    path("m/", include("msgr.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
