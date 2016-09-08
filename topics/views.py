from django.shortcuts import render
from reactions.models import Reaction


def index(request):
    topic_list = Reaction.objects.filter(topic=None).order_by('-id')
    return render(request, 'topics/index.html', {
        'topic_list': topic_list,
    })
