
import re

from django import template
from django.template.defaultfilters import stringfilter
from django.urls import reverse
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from accounts.models import Profile


register = template.Library()


def get_link(match):
    """Form the HTML anchor tag to the users' profiles."""

    identifier = match.group()
    profile = Profile.objects.filter(identifier__iexact=identifier[1:])
    if profile.count() == 1:
        # If user exists
        profile = profile.get()
        url = reverse("msgr:profile", args=[profile.pk])
    else:
        url = ""
    link = '<a href="%s">%s</a>' % (url, identifier)
    return link


@register.filter(needs_autoescape=True)
@stringfilter
def inline_id(text, autoescape=True):
    """Convert all words starting with an '@' character to
    inline links to profiles of users with those IDs (if exist).
    """

    if autoescape:
        text = conditional_escape(text)
    text = re.sub("@\w{5,}", get_link, text)
    return mark_safe(text)
