from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from reactions.models import Reaction
from .forms import TopicForm


def index(request):
    topic_list = Reaction.objects.filter(target=None, deleted=False).order_by('-id')
    form = TopicForm()
    return render(request, 'topics/index.html', {
        'topic_list': topic_list,
        'form': form,
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
