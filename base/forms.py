from django import forms
from .models import Room, Message

class RoomForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput
                           (attrs={'placeholder':'E.g. Mastering Python + Django'}))
    # description = forms.CharField(widget=forms.TextInput
    #                        (attrs={'placeholder':'Write about your study group...'}))
    class Meta:
        model = Room
        fields = ('topic', 'name', 'description')



class MessageForm(forms.ModelForm):
    body = forms.CharField(widget=forms.TextInput
                           (attrs={'placeholder':'Write a message...'}))
    class Meta:
        model = Message
        fields = ('body',)


