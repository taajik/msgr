
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View, ListView, DetailView

from .models import Chat
from accounts.models import Profile


User = get_user_model()


class ChatsListView(ListView):
    """Main page list of a user's chat entries."""

    template_name = "msgr/chats_list.html"

    def get_queryset(self):
        return self.request.user.joins.order_by("chat__lat")


class ProfilePageView(DetailView):
    """Profile page of a user to display their general info."""

    template_name = "msgr/profile_page.html"

    def get_queryset(self):
        return Profile.objects.filter(pk=self.kwargs["pk"])


class StartChatView(View):
    """Create a private chat between the logged-in user and another.

    The other user is identified using its profile pk,
    that is passed in the url pattern.
    """

    def post(self, request, *args, **kwargs):
        other = User.objects.get(profile__pk=kwargs["pk"])
        chat = Chat.objects.filter(participants=request.user)
        chat = chat.filter(participants=other)
        if not chat:
            chat = Chat.objects.create()
            chat.participants.set([request.user, other])
        else:
            chat.get()
        return HttpResponseRedirect(reverse("msgr:main"))
