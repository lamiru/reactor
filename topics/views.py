from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from reactions.models import Reaction
from .forms import TopicForm


def index(request):
    topic_list = Reaction.objects.filter(topic=None).order_by('-id')
    return render(request, 'topics/index.html', {
        'topic_list': topic_list,
    })


@login_required
def new(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.actor = request.user
            topic.good_score = 0
            topic.pass_score = 0
            topic.save()
            return redirect('topics:index')
    else:
        form = TopicForm()
    return render(request, '_form.html', {
        'form': form,
    })
