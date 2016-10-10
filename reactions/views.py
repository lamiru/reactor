from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Reaction


@login_required
def detail(request, pk):
    reaction = get_object_or_404(Reaction, pk=pk)

    tree = reaction.get_tree()
    children = reaction.get_children()
    brothers = reaction.get_brothers()
    parents = reaction.get_parents()

    if parents is None:
        lists = [brothers, children, [],]
    else:
        lists = [parents, brothers, children,]

    return render(request, 'reactions/detail.html', {
        'tree': tree,
        'lists': lists,
    })
