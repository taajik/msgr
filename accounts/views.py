
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import CreateView, UpdateView

from .forms import UserCreationForm, ProfileForm
from .models import Profile


class SignupView(CreateView):
    """Display the sign up form and create a user."""

    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_anonymous:
            return HttpResponseRedirect(reverse("profile"))
        return super().dispatch(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, UpdateView):
    """Display profile fields of the currently logged in user for edit."""

    form_class = ProfileForm
    success_url = reverse_lazy("profile")
    login_url = reverse_lazy("login")
    template_name = "registration/profile.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)
