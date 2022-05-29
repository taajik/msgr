
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q, Count, CharField, Value as V
from django.db.models.functions import Concat
from django.http import (
    Http404,
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import (
    DetailView,
    ListView,
    View,
)
from django.views.generic.list import MultipleObjectMixin

from .forms import SearchForm, MessageForm
from .models import Chat, Message
from accounts.models import Profile


class SearchFormMixin:
    """Include the form context data for search_form.html inclusion."""

    def get_search_form(self):
        kwargs = {}
        if self.request.GET:
            kwargs = {"data": self.request.GET}
        return SearchForm(**kwargs)

    def get_context_data(self, **kwargs):
        kwargs["search_form"] = self.get_search_form()
        return super().get_context_data(**kwargs)


class ChatsListView(SearchFormMixin, ListView):
    """Main page list of a user's chat entries."""

    template_name = "msgr/chats_list.html"

    def get_queryset(self):
        return self.request.user.joins.order_by("-chat__lat")


class SearchView(SearchFormMixin, ListView):
    """Result page of searching for users."""

    template_name = "msgr/search_page.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            # Search in full name or id.
            queryset = Profile.objects.annotate(
                full_name=Concat(
                    "first_name", V(" "), "last_name",
                    output_field=CharField()
                )
            )
            return queryset.filter(
                Q(full_name__icontains=query) | Q(identifier__icontains=query)
            )
        else:
            return Profile.objects.none()


class ProfilePageView(DetailView):
    """Profile page of a user to display their general info."""

    template_name = "msgr/profile_page.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, pk=self.kwargs["pk"])

    def post(self, request, *args, **kwargs):
        """Start and enter a chat between two users."""
        # Get all chats in which the logged-in user participates.
        chats = Chat.objects.annotate(Count("participants", distinct=True))
        chats = chats.filter(participants=request.user)
        other = self.get_object().user

        if request.user == other:
            # If this is the user's own profile,
            # find the "saved messages" chat.
            chats = chats.filter(participants__count=1)
        else:
            # Otherwise find the chat between
            # the two users, if there is one.
            chats = chats.filter(participants=other)

        if chats:
            # If a chat already exists, use that one to redirect to.
            chat = chats.get()
        else:
            # Otherwise create a private chat between
            # the logged-in user and the other user.
            chat = Chat.objects.create()
            chat.participants.set([request.user, other])

        return HttpResponseRedirect(reverse("msgr:chat", args=[chat.pk]))


class ChatView(UserPassesTestMixin, DetailView):
    """A chat page that contains messages."""

    template_name = "msgr/chat_page.html"
    permission_denied_message = "Sorry, you can't access this chat."
    raise_exception = True

    def get_object(self, queryset=None):
        return get_object_or_404(Chat, pk=self.kwargs["pk"])

    def test_func(self):
        """Only users that are in this chat can access this page."""
        self.object = self.get_object()
        return self.object.participants.filter(pk=self.request.user.pk).exists()

    def post(self, request, *args, **kwargs):
        """Save a new message and record user's activity."""
        if request.POST.get("content"):
            # If it's a new message from submit, create the message.
            form = self.get_form({"data": request.POST})
            if form.is_valid():
                message = form.save(commit=False)
                message.chat = self.object
                message.sender = request.user
                message.save()
                # A new activity has happened in the chat, so:
                self.object.update_lat()
                return HttpResponse(status=204)
            else:
                return HttpResponse("message wasn't sent",
                                    content_type="text/plain",
                                    status=400)
        else:
            # Otherwise if a post request is sent
            # without any parameters (except the csrf token),
            # it means that the user has exited the chat page.
            request.user.joins.get(chat=self.object).update_last_active()
            return HttpResponse(status=204)

    def get_form(self, kwargs=None):
        if kwargs is None:
            kwargs = {}
        return MessageForm(**kwargs)

    def get_context_data(self, **kwargs):
        if "form" not in kwargs:
            kwargs["form"] = self.get_form()
        return super().get_context_data(**kwargs)


class ChatMessagesView(UserPassesTestMixin, MultipleObjectMixin, View):
    """Paginate messages and return rendered result in json."""

    paginate_by = 20

    def get_chat(self):
        return get_object_or_404(Chat, pk=self.kwargs["pk"])

    def test_func(self):
        self.chat = self.get_chat()
        return self.chat.participants.filter(pk=self.request.user.pk).exists()

    def get_queryset(self):
        return self.chat.messages.reverse()

    def get(self, request, *args, **kwargs):
        # The full queryset:
        self.object_list = self.get_queryset()
        try:
            context = self.get_context_data()
        except Http404:
            # A 404 error breaks the chat; so instead send an empty response.
            return JsonResponse({"messages_rendered": ""})
        context["user"] = request.user
        messages_rendered = render_to_string(
            "msgr/messages_list.html",
            context=context,
        )

        # This page of the queryset:
        object_list = context["object_list"]
        # Include the primary key of the first item
        # on the page in json response.
        first_item_pk = "0"
        if object_list.exists():
            first_item_pk = object_list.first().pk
            # Fetching this page means its messages are seen:
            self.object_list.filter(pk__in=object_list).exclude(
                sender=request.user
            ).update(is_seen=True)
        return JsonResponse({
            "messages_rendered": messages_rendered,
            "first_item_pk": first_item_pk,
        })


class ChatUpdatesView(UserPassesTestMixin, View):
    """Return updates about a chat in json."""

    def get_chat(self):
        return get_object_or_404(Chat, pk=self.kwargs["pk"])

    def test_func(self):
        self.chat = self.get_chat()
        return self.chat.participants.filter(pk=self.request.user.pk).exists()

    def get(self, request, *args, **kwargs):
        if request.GET:
            response = self.get_updates(request.GET.get("latest_pk"),
                                        request.GET.get("latest_seen_pk"))
            return JsonResponse(response)
        else:
            raise Http404

    def get_updates(self, latest_pk, latest_seen_pk):
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

        if not latest_pk:
            latest_pk = "0"
        new_messages = self.chat.messages.filter(pk__gt=latest_pk)
        new_messages_rendered = ""

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

        if not latest_seen_pk:
            latest_seen_pk = "0"
        seen_messages = self.chat.messages.filter(pk__gt=latest_seen_pk,
                                                  sender=self.request.user,
                                                  is_seen=True)
        seen_messages_pk = []

        if seen_messages.exists():
            seen_messages_pk = [m.pk for m in seen_messages]
            latest_seen_pk = seen_messages_pk[-1]
        return seen_messages_pk, latest_seen_pk


class ChatDeleteMessageView(View):
    """Delete a user's message with no response."""

    def post(self, request, *args, **kwargs):
        message = get_object_or_404(Message, pk=request.POST.get("message"))
        # A user can only delete their own message.
        if request.user == message.sender:
            message.delete()
        return HttpResponse(status=204)
