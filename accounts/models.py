
import re

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


def validate_id(value):
    """Check if a user's id matches some criteria."""

    if not re.match(".{5,}", value):
        raise ValidationError("ID is too short.")
    if not re.match("(?!.*__.*)[a-zA-Z][\w_]*[^_ ]$", value):
        raise ValidationError("ID is invalid.")

class Profile(models.Model):
    """A user's profile informations."""

    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name="profile", verbose_name="user")
    first_name = models.CharField(default="new user", max_length=30)
    last_name = models.CharField(blank=True, max_length=30)
    email_address = models.EmailField("email", unique=True,
                                      blank=True, null=True)
    identifier = models.CharField("id", unique=True, blank=True,
                                  null=True, max_length=30,
                                  validators=[validate_id])
    biography = models.CharField("bio", blank=True, max_length=200)

    def __str__(self) -> str:
        return "%s's profile" % self.user.username
