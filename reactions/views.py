from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Sum
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
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

    form = ReactionForm()

    return render(request, 'reactions/detail.html', {
        'tree': tree,
        'lists': lists,
        'current_reaction': current_reaction,
        'current_rate': current_rate,
        'form': form,
    })


@login_required
def detail_s(request, pk):
    return redirect('reactions:detail', pk)


@login_required
def ranking(request, pk):
    topic = get_object_or_404(Reaction, pk=pk)
    if not topic == topic.topic:
        return redirect('reactions:ranking', topic.topic)

    score_by_actor = User.objects.filter(reaction__topic=topic) \
        .annotate(score=Sum('reaction__score')) \
        .order_by('-score')[:10]

    return render(request, 'reactions/ranking.html', {
        'score_by_actor': score_by_actor,
    })


@login_required
def rate_good(request, pk):
    if request.method == 'POST':
        reaction = get_object_or_404(Reaction, pk=pk)
        topic = reaction.topic
        try:
            Rate.objects.create(user=request.user, topic=topic, reaction=reaction, rate='G')
            reaction.score += 1
            reaction.save()
        except IntegrityError:
            rate = Rate.objects.get(user=request.user, reaction=reaction)
            if rate.rate == 'P':
                rate.rate = 'G'
                reaction.score += 1
                reaction.save()
                rate.save()
        return redirect('reactions:detail', pk)
    else:
        return Http404()


@login_required
def rate_pass(request, pk):
    if request.method == 'POST':
        reaction = get_object_or_404(Reaction, pk=pk)
        topic = reaction.topic
        try:
            Rate.objects.create(user=request.user, topic=topic, reaction=reaction, rate='P')
        except IntegrityError:
            rate = Rate.objects.get(user=request.user, reaction=reaction)
            if rate.rate == 'G':
                rate.rate = 'P'
                reaction.score -= 1
                reaction.save()
                rate.save()
        return redirect('reactions:detail', pk)
    else:
        return Http404()


@login_required
def reaction_new(request, pk):
    if request.method == 'POST':
        form = ReactionForm(request.POST)
        if form.is_valid():
            target = get_object_or_404(Reaction, pk=pk)
            get_object_or_404(Rate, user=request.user, reaction=pk)
            reaction = form.save(commit=False)
            reaction.actor = request.user
            reaction.target = target
            reaction.topic = target.topic
            reaction.save()
            return redirect('reactions:detail', reaction.pk)
    raise Http404()


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
