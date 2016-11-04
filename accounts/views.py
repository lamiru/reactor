from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import FormView
from languages import trans as _
from .forms import *
from .models import *
from reactions.models import Reaction


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
        context['submit'] = _('login')
        context['next'] = self.request.GET.get('next') and self.request.GET.get('next') or ''
        return context

    def form_valid(self, form):
        user = form.get_user()
        auth_login(self.request, user)
        return super(LoginView, self).form_valid(form)


def login_s(request):
    next_url = request.GET.get('next') and '?next=' + request.GET.get('next') or ''
    return redirect('/login' + next_url)


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            auth_login(request, user)
            messages.info(request, "Thanks for registering. You are now logged in.")
            next_url = request.GET.get('next', 'accounts:index')
            return redirect(next_url)
    else:
        form = SignupForm()
    return render(request, '_form.html', {
        'form': form,
    })


@login_required
def my_reactions(request):
    my_reactions = Reaction.objects.filter(actor=request.user)
    topics = []
    for reaction in my_reactions:
        if reaction.topic not in topics:
            reaction.topic.my_reactions = \
                my_reactions.filter(topic=reaction.topic, target__isnull=False)
            topics.append(reaction.topic)

    topics.sort(key=lambda item: item.pk, reverse=True)

    paginator = Paginator(topics, 10)
    page = request.GET.get('page')
    try:
        topic_list = paginator.page(page)
    except PageNotAnInteger:
        topic_list = paginator.page(1)
    except EmptyPage:
        topic_list = paginator.page(paginator.num_pages)

    return render(request, 'accounts/my_reactions.html', {
        'topic_list': topic_list,
    })


@login_required
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
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
        'submit': _('save')
    })


@login_required
def index(request):
    return redirect('topics:index')
