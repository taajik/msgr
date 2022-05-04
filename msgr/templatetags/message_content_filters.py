
import re

from django import template
from django.template.defaultfilters import stringfilter
from django.urls import reverse
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from accounts.models import Profile


register = template.Library()


def get_link(match):
    identifier = match.group()
    profile = Profile.objects.filter(identifier__iexact=identifier[1:])
    if profile.count() == 1:
        profile = profile.get()
        url = reverse("msgr:profile", args=[profile.pk])
    else:
        url = ""
    link = '<a href="%s">%s</a>' % (url, identifier)
    return link


@register.filter(needs_autoescape=True)
@stringfilter
def inline_id(text, autoescape=True):
    if autoescape:
        text = conditional_escape(text)
    text = re.sub("@\w{5,}", get_link, text)
    return mark_safe(text)
