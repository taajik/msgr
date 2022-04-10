
from django.views.generic import ListView, DetailView

from accounts.models import Profile


class ChatsView(ListView):
    """Main page list of a user's chat entries."""

    template_name = "msgr/chats_list.html"

    def get_queryset(self):
        return self.request.user.joins.order_by("chat__lat")


class ProfilePageView(DetailView):
    """Profile page of a user to display their general info."""

    template_name = "msgr/profile_page.html"

    def get_queryset(self):
        return Profile.objects.filter(pk=self.kwargs["pk"])
