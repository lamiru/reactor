from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Reaction


@login_required
def detail(request, pk):
    reaction = get_object_or_404(Reaction, pk=pk)
    reaction_list = []
    reaction_list.append(reaction)

    for reaction in reaction_list:
        if reaction.target is not None:
            reaction = reaction.target
            reaction_list.append(reaction)

    return render(request, 'reactions/detail.html', {
        'reaction_list': reaction_list,
    })
