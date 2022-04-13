
from django import forms

from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = (
            "content",
        )
        widgets = {
            "content": forms.TextInput(attrs={
                "id": "message-content",
                "required": True,
                "placeholder": "Message..."
            }),
        }
