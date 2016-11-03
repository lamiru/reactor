from django import forms
from django.utils.translation import ugettext_lazy as _


class SearchForm(forms.Form):
    q = forms.CharField(
        max_length = 20,
        widget = forms.TextInput(attrs={'placeholder': _('Search')}),
    )
