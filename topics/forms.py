from django import forms
from reactions.models import Reaction


class TopicForm(forms.ModelForm):
    class Meta:
        model = Reaction
        fields = ('title', 'contents',)
