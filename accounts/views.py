from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views.generic import FormView
from .forms import *


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
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = ProfileForm(instance=request.user)
    return render(request, '_form.html', {
        'form': form,
    })


@login_required
def index(request):
    return render(request, 'accounts/index.html', {
    })
