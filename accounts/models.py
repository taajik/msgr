
import re

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class UserManager(BaseUserManager):
    """Custom user model manager with email as the unique identifier."""

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom user model with only email and password fields."""

    username = None
    first_name = None
    last_name = None
    email = models.EmailField("email address", unique=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.email


def validate_id(value):
    """Check if a user's id matches some criteria."""

    if not re.match(".{5,}", value):
        raise ValidationError("ID is too short.")
    if not re.match("(?!.*__.*)[a-zA-Z][\w_]*[^_ ]$", value):
        raise ValidationError("ID is invalid.")


class Profile(models.Model):
    """A user's profile informations."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, default="new user")
    last_name = models.CharField(max_length=30, blank=True)
    identifier = models.CharField("id", max_length=30,
                                  unique=True, blank=True, null=True,
                                  validators=[validate_id])
    biography = models.CharField("bio", max_length=200, blank=True)

    def __str__(self) -> str:
        return "%s profile" % self.user.get_username()
