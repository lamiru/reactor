from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Reaction


@login_required
def detail(request, pk):
    reaction = get_object_or_404(Reaction, pk=pk)
    list_3 = reaction.target_reactions.all()
    reaction_tree = []
    reaction_tree.append(reaction)

    for reaction in reaction_tree:
        if reaction.target is not None:
            reaction = reaction.target
            reaction_tree.append(reaction)

    try:
        list_2 = reaction_tree[1].target_reactions.all()
    except:
        list_2 = None
    try:
        list_1 = reaction_tree[2].target_reactions.all()
    except:
        list_1 = None
    print(reaction_tree)

    return render(request, 'reactions/detail.html', {
        'reaction_tree': reaction_tree,
        'list_3': list_3,
        'list_2': list_2,
        'list_1': list_1,
    })
