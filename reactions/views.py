from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import *


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

    current_rate = None
    try:
        rate = Rate.objects.get(user=request.user, reaction=current_reaction)
        if rate.rate == 'G':
            current_rate = 'Good'
        else:
            current_rate = 'Pass'
    except ObjectDoesNotExist:
        current_rate = None

    return render(request, 'reactions/detail.html', {
        'tree': tree,
        'lists': lists,
        'current_reaction': current_reaction,
        'current_rate': current_rate,
    })


@login_required
def rate_good(request, pk):
    if request.method == 'POST':
        reaction = get_object_or_404(Reaction, pk=pk)
        try:
            if reaction.topic is None:
                topic = reaction
            else:
                topic = reaction.topic
            Rate.objects.create(user=request.user, topic=topic, reaction=reaction, rate='G')
            reaction.score += 1
            reaction.save()
        except IntegrityError:
            messages.error(request, "You have already rated this reaction.")
        return redirect('reactions:detail', pk)
    else:
        return Http404()


@login_required
def rate_pass(request, pk):
    if request.method == 'POST':
        reaction = get_object_or_404(Reaction, pk=pk)
        try:
            if reaction.topic is None:
                topic = reaction
            else:
                topic = reaction.topic
            Rate.objects.create(user=request.user, topic=topic, reaction=reaction, rate='P')
        except IntegrityError:
            messages.error(request, "You have already rated this reaction.")
        return redirect('reactions:detail', pk)
    else:
        return Http404()


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
