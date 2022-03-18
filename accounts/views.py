
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import ProfileForm
from .models import Profile


class SignupView(CreateView):
    """Display the sign up form and create a user."""

    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    # todo: decorators like the auth.LoginView
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_anonymous:
            return HttpResponseRedirect(reverse("home"))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Before redirecting, create a profile
        for the successfully created user.
        """

        response = super().form_valid(form)
        profile_form = ProfileForm()
        profile_obj = profile_form.save(commit=False)
        profile_obj.user = self.object
        profile_obj.save()

        return response


class ProfileView(LoginRequiredMixin, UpdateView):
    """Display the profile of the currently logged in user for editing."""

    form_class = ProfileForm
    success_url = reverse_lazy("profile")
    login_url = reverse_lazy("login")
    template_name = "registration/profile.html"

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)
