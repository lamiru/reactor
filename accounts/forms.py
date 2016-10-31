from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from languages import trans as _
from .models import *


class SignupForm(UserCreationForm):
    username = forms.RegexField(
        label=_('username'),
        max_length=20,
        regex=r'^[\w_]+$',
        help_text = "Required. 20 characters or fewer. Letters, digits and _ only.",
        error_messages = {
            'invalid': "This value may contain only letters, numbers and _ characters."
        }
    )
    email = forms.EmailField(
        label=_('email'),
    )

    def clean_email(self):
        email = self.cleaned_data.get('email').strip()
        if email:
            if User.objects.filter(email=email).exists() == True:
                raise forms.ValidationError('This email is already used.')
        return email

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserForm(forms.ModelForm):
    email = forms.EmailField(
        label=_('email'),
    )
    class Meta:
        model = User
        fields = ('email', 'last_name', 'first_name',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('about', 'photo',)
