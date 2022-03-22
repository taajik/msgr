
from django.views.generic import DetailView

from accounts.models import Profile


class ProfilePageView(DetailView):
    """Profile page of a user to display their general info."""

    template_name = "msgr/profile_page.html"

    def get_queryset(self):
        return Profile.objects.filter(pk=self.kwargs["pk"])
