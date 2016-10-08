from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import FormView
from .forms import *
from .models import *


class LoginView(FormView):
    template_name = '_form.html'
    form_class = AuthenticationForm

    def get_success_url(self):
       next_url = self.request.POST.get('next')
       if next_url:
           return '%s' % (next_url)
       else :
           return reverse_lazy('accounts:index')

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['submit'] = 'Log in'
        context['next'] = self.request.GET.get('next') and self.request.GET.get('next') or ''
        return context

    def form_valid(self, form):
        user = form.get_user()
        auth_login(self.request, user)
        return super(LoginView, self).form_valid(form)


@login_required
def profile(request):
    user_profile, is_created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        uform = UserForm(request.POST, instance=request.user)
        pform = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if uform.is_valid() and pform.is_valid():
            uform.save()
            pform.save()
            return redirect('accounts:profile')
    else:
        uform = UserForm(instance=request.user)
        pform = UserProfileForm(instance=user_profile)
    return render(request, 'accounts/profile.html', {
        'uform': uform,
        'pform': pform,
    })


@login_required
def index(request):
    return render(request, 'accounts/index.html', {
    })
