from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Reaction


@login_required
def detail(request, pk):
    current_reaction = get_object_or_404(Reaction, pk=pk)
    reaction = current_reaction
    reaction_list = []
    if reaction.target:
        reaction_list.append(reaction.target)
    for i in reaction_list:
        reaction = Reaction.objects.get(pk=i.pk)
        if reaction.target:
            reaction_list.append(reaction.target)
    reaction_list.insert(0, current_reaction)
    return render(request, 'reactions/detail.html', {
        'reaction_list': reaction_list,
    })
