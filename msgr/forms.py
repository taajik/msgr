
from django import forms

from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = (
            "content",
        )
        widgets = {
            "content": forms.Textarea(attrs={
                "id": "message-field",
                "required": True,
                "placeholder": "Message...",
                "rows": "1",
            }),
        }
