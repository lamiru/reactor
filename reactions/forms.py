from django import forms
from .models import Reaction


class ReactionForm(forms.ModelForm):
    class Meta:
        model = Reaction
        fields = (
            'title', 'contents',
            'url', 'url_title', 'url_description', 'url_image'
        )
