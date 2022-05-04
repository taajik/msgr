
from django import forms
from django.contrib.auth.forms import (
    UserCreationForm as BaseUserCreationForm,
    UserChangeForm as BaseUserChangeForm,
)

from .models import User, Profile


class UserCreationForm(BaseUserCreationForm):

    class Meta:
        model = User
        fields = ("email",)


class UserChangeForm(BaseUserChangeForm):

    class Meta:
        model = User
        fields = "__all__"


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = (
            "first_name",
            "last_name",
            "identifier",
            "biography",
        )
