from django import forms
from .models import GroupMessage, ChatGroup
from django.contrib.auth.models import User

class ChatMessageCreateForm(forms.ModelForm):
    class Meta:
        model = GroupMessage
        fields = ['body']  # Assuming 'body' is the field for the message content
        widgets ={
            'body': forms.TextInput(attrs={'placeholder': 'add message ...','class':'p-4 text-black', 'maxlength': '300','autofocus':True}),
        }