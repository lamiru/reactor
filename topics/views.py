from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from reactions.models import Reaction
from .forms import *


def index(request):
    topic_list = Reaction.objects.filter(target=None, deleted=False).order_by('-id')
    tform = TopicForm()
    sform = SearchForm()
    return render(request, 'topics/index.html', {
        'topic_list': topic_list,
        'tform': tform,
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
    topic_list = title_list | contents_list

    return render(request, 'topics/search.html', {
        'topic_list': topic_list,
    })


@login_required
def new(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.actor = request.user
            topic.score = 0
            topic.save()
            topic = Reaction.objects.get(pk=topic.pk)
            topic.topic = topic
            topic.save()
            return redirect('topics:index')
    raise Http404()
