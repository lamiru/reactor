from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from reactions.models import Reaction
from .forms import TopicForm


def index(request):
    topic_list = Reaction.objects.filter(topic=None).order_by('-id')
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
            return redirect('topics:index')
    raise Http404()


@login_required
def delete(request, pk):
    if request.method == 'POST':
        topic = get_object_or_404(Reaction, pk=pk)
        if (not request.user.is_staff) and topic.actor != request.user:
            messages.error(request, "You don't have permission.")
        else:
            topic.delete()
        return redirect('topics:index')
    raise Http404()
