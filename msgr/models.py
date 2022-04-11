
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
