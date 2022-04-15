
from functools import cached_property

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    View,
    TemplateView,
    DetailView,
    ListView,
)

from .forms import MessageForm
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

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, pk=self.kwargs["pk"])


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


class ChatView(UserPassesTestMixin, TemplateView):
    """A chat page that contains messages."""

    template_name = "msgr/chat_page.html"
    permission_denied_message = "Sorry, you can't access this chat."
    raise_exception = True

    @cached_property
    def chat(self):
        return get_object_or_404(Chat, pk=self.kwargs["pk"])

    def test_func(self):
        return self.chat.participants.filter(pk=self.request.user.pk).exists()

    def get(self, request, *args, **kwargs):
        if request.GET.get("update"):
            messages = self.get_queryset(request.GET.get("latest_pk"))
            response = render_to_string("msgr/messages_list.html", {
                "message_list": messages,
                "user": request.user,
            })
            return JsonResponse({"message_items": response,
                                 "latest_pk": getattr(messages.last(), "pk", 0)})
        else:
            return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form({"data": request.POST})
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = self.chat
            message.sender = request.user
            message.save()
            self.chat.update_lat()
            return HttpResponse(status=204)
        else:
            return HttpResponse("message wasn't sent",
                                content_type="text/plain",
                                status=400)

    def get_queryset(self, latest_pk=0):
        messages = self.chat.messages.filter(pk__gt=latest_pk)
        messages.exclude(sender=self.request.user).update(is_seen=True)
        return messages

    def get_form(self, kwargs=None):
        if kwargs is None:
            kwargs = {}
        return MessageForm(**kwargs)

    def get_context_data(self, **kwargs):
        kwargs["chat"] = self.chat
        if "form" not in kwargs:
            kwargs["form"] = self.get_form()
        return super().get_context_data(**kwargs)
