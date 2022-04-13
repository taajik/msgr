
from django.conf import settings
from django.db import models
from django.utils import timezone


class Chat(models.Model):
    """Parent model representing a chat between multiple users.

    Direct instances of this class are private messages; which means
    the 'participants' relationship should only include two users.
    """

    participants = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                          through="Join", blank=True,
                                          related_name="chats")
    lat = models.DateTimeField("latest activity time", default=timezone.now)

    def update_lat(self):
        self.lat = timezone.now()
        self.save()

    def __str__(self) -> str:
        return "chat object (%s)" % self.pk


class Join(models.Model):
    """Intermediate model for relations between a user and a chat."""

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="+")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="joins")
    date_joined = models.DateField(auto_now_add=True)
    unread_count = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("user", "chat"),
                name="user_join_once_constraint"
            )
        ]

    def get_receivers(self):
        """Return all other users that are in the same chat."""
        return self.chat.participants.exclude(pk=self.user.pk)

    @property
    def title(self):
        """Return a title for the chat's entry"""
        return self.get_receivers().get().profile.get_full_name()


class Message(models.Model):
    """A message sent in a chat.

    Only the 'sender' is specified because 'chat' works as receivers,
    since audiences of a message are anyone else in the same chat.
    """

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE,
                             related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name="+")
    content = models.TextField()
    send_time = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

    class Meta:
        ordering = ["send_time"]

    def __str__(self) -> str:
        return "chat (%s) message by %s" % (self.chat.pk,
                                          self.sender.get_username())
