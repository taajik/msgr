
from functools import cached_property

from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    TemplateView,
    DetailView,
    ListView,
)

from .forms import MessageForm
from .models import Chat
from accounts.models import Profile


class ChatsListView(ListView):
    """Main page list of a user's chat entries."""

    template_name = "msgr/chats_list.html"

    def get_queryset(self):
        return self.request.user.joins.order_by("-chat__lat")


class ProfilePageView(DetailView):
    """Profile page of a user to display their general info."""

    template_name = "msgr/profile_page.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, pk=self.kwargs["pk"])

    def post(self, request, *args, **kwargs):
        """Create a private chat between the logged-in user and this use
        if one doesn't already exists."""

        other = self.get_object().user
        chat = Chat.objects.filter(participants=request.user)
        chat = chat.filter(participants=other)
        if not chat:
            chat = Chat.objects.create()
            chat.participants.set([request.user, other])
        else:
            chat = chat.get()

        return HttpResponseRedirect(reverse("msgr:chat", args=[chat.pk]))


class ChatView(UserPassesTestMixin, TemplateView):
    """A chat page that contains messages."""

    template_name = "msgr/chat_page.html"
    permission_denied_message = "Sorry, you can't access this chat."
    raise_exception = True

    @cached_property
    def chat(self):
        """The corresponding chat object."""
        return get_object_or_404(Chat, pk=self.kwargs["pk"])

    def test_func(self):
        """Only users that are in this chat can access this page."""
        return self.chat.participants.filter(pk=self.request.user.pk).exists()

    def get(self, request, *args, **kwargs):
        if request.GET:
            # If there are GET parameters, use them to
            # return updates about this chat.
            response = self.get_updates(request.GET.get("latest_pk"),
                                        request.GET.get("latest_seen_pk"))
            return JsonResponse(response)
        else:
            # Otherwise if the url is simply requested,
            # return the rendered chat page.
            return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.POST.get("content"):
            # If it's a new message from, create the message.
            form = self.get_form({"data": request.POST})
            if form.is_valid():
                message = form.save(commit=False)
                message.chat = self.chat
                message.sender = request.user
                message.save()
                # A new activity has happened in the chat, so:
                self.chat.update_lat()
                return HttpResponse(status=204)
            else:
                return HttpResponse("message wasn't sent",
                                    content_type="text/plain",
                                    status=400)
        else:
            # Otherwise if a post request is sent
            # without any parameters (except the csrf token),
            # it means that the user has exited the chat page.
            request.user.joins.get(chat=self.chat).update_last_active()
            return HttpResponse(status=204)

    def get_updates(self, latest_pk=0, latest_seen_pk=0):
        """Get updates according to provided arguments.

        latest_pk is the most recent message that one has got. and
        latest_seen_pk is the latest message marked as seen.

        Return a dictionary containing updates,
        that can be used as a json response.
        This dictionary includes updated values for the arguments that
        can be used in later calls to the method.
        """

        new_messages_rendered, latest_pk = self.get_new_messages(latest_pk)
        seen_messages_pk, latest_seen_pk = self.get_seen_messages(latest_seen_pk)
        return {
            "new_messages_rendered": new_messages_rendered,
            "latest_pk": latest_pk,
            "seen_messages_pk": seen_messages_pk,
            "latest_seen_pk": latest_seen_pk,
        }

    def get_new_messages(self, latest_pk):
        """Get all messages in this chat that
        have been sent after the given.

        Return rendered html of all new messages and
        primary key of the last one (updated latest_pk).
        """

        new_messages = self.chat.messages.filter(pk__gt=latest_pk)
        new_messages_rendered = ""
        latest_pk = 0
        if new_messages.exists():
            # Fetching these messages means they are seen:
            new_messages.exclude(sender=self.request.user).update(is_seen=True)
            new_messages_rendered = render_to_string(
                "msgr/messages_list.html",
                context={
                    "message_list": new_messages.reverse(),
                    "user": self.request.user,
                },
            )
            latest_pk = new_messages.last().pk
        return new_messages_rendered, latest_pk

    def get_seen_messages(self, latest_seen_pk):
        """Get all messages in this chat that
        have been seen since the given.

        Return list of all new messages' primary keys and
        primary key of the last one (updated latest_seen_pk).
        """

        seen_messages = self.chat.messages.filter(pk__gt=latest_seen_pk,
                                                  sender=self.request.user,
                                                  is_seen=True)
        seen_messages_pk = []
        latest_seen_pk = 0
        if seen_messages.exists():
            seen_messages_pk = [m.pk for m in seen_messages]
            latest_seen_pk = seen_messages_pk[-1]
        return seen_messages_pk, latest_seen_pk

    def get_form(self, kwargs=None):
        if kwargs is None:
            kwargs = {}
        return MessageForm(**kwargs)

    def get_context_data(self, **kwargs):
        kwargs["chat"] = self.chat
        if "form" not in kwargs:
            kwargs["form"] = self.get_form()
        return super().get_context_data(**kwargs)
