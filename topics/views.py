from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.shortcuts import render, redirect, get_list_or_404
from reactions.models import Reaction
from reactions.forms import ReactionForm
from .forms import *


def index(request):
    topics = Reaction.objects.filter(target=None, deleted=False).order_by('-id')
    paginator = Paginator(topics, 10)
    page = request.GET.get('page')
    try:
        topic_list = paginator.page(page)
    except PageNotAnInteger:
        topic_list = paginator.page(1)
    except EmptyPage:
        topic_list = paginator.page(paginator.num_pages)

    rform = ReactionForm()
    sform = SearchForm()

    return render(request, 'topics/index.html', {
        'topic_list': topic_list,
        'rform': rform,
        'sform': sform,
    })


def search(request):
    if not 'q' in request.GET:
        return redirect ('topics:index')
    query = request.GET['q']

    title_list = Reaction.objects.filter(
        target=None, deleted=False, title__contains=query
    ).order_by('-id')
    contents_list = Reaction.objects.filter(
        target=None, deleted=False, contents__contains=query
    ).order_by('-id')
    topics = title_list | contents_list
    paginator = Paginator(topics, 10)
    page = request.GET.get('page')
    try:
        topic_list = paginator.page(page)
    except PageNotAnInteger:
        topic_list = paginator.page(1)
    except EmptyPage:
        topic_list = paginator.page(paginator.num_pages)

    rform = ReactionForm()
    sform = SearchForm(initial=request.GET)

    return render(request, 'topics/search.html', {
        'topic_list': topic_list,
        'rform': rform,
        'sform': sform,
    })


@login_required
def new(request):
    if request.method == 'POST':
        form = ReactionForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.actor = request.user
            topic.score = 0
            topic.save()
            topic.topic = topic
            topic.save()
            return redirect('topics:index')
    raise Http404()
