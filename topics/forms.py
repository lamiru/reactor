from django import forms
from reactions.models import Reaction


class TopicForm(forms.ModelForm):
    class Meta:
        model = Reaction
        fields = ('title', 'contents',)


class SearchForm(forms.Form):
    q = forms.CharField(
        max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Search'})
    )
