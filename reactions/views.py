from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Reaction


@login_required
def detail(request, pk):
    current_reaction = get_object_or_404(Reaction, pk=pk)

    tree = current_reaction.get_tree()
    children = current_reaction.get_children()
    brothers = current_reaction.get_brothers()
    parents = current_reaction.get_parents()

    if parents is None:
        lists = [brothers, children, [],]
    else:
        lists = [parents, brothers, children,]

    return render(request, 'reactions/detail.html', {
        'tree': tree,
        'lists': lists,
        'current_reaction': current_reaction,
    })


@login_required
def delete(request, pk):
    reaction = get_object_or_404(Reaction, pk=pk)
    if (not request.user.is_staff) and reaction.actor != request.user:
        messages.error(request, "You don't have permission.")
    else:
        if request.method == 'POST':
            reaction.deleted = True
            reaction.save()
        else:
            return render(request, 'reactions/delete.html', {
                'reaction': reaction,
            })
    return redirect('topics:index')
