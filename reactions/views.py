from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Sum
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from helpers.score import calculate_score
from .forms import *
from .models import *


@login_required
def detail(request, pk):
    current_reaction = get_object_or_404(Reaction, pk=pk)

    tree = current_reaction.get_tree()
    next_generation = current_reaction.get_next_generation()
    current_generation = current_reaction.get_current_generation()
    previous_generation = current_reaction.get_previous_generation()
    if previous_generation is None:
        g_title = ['Current', 'Next', '']
        generations = [current_generation, next_generation, [],]
    else:
        g_title = ['Previous', 'Current', 'Next',]
        generations = [previous_generation, current_generation, next_generation,]

    try:
        rating = Rating.objects.get(user=request.user, reaction=current_reaction).rating
    except ObjectDoesNotExist:
        rating = None

    form = ReactionForm()

    return render(request, 'reactions/detail.html', {
        'tree': tree,
        'g_title': g_title,
        'generations': generations,
        'current_reaction': current_reaction,
        'rating': rating,
        'form': form,
    })


@login_required
def detail_s(request, pk):
    return redirect('reactions:detail', pk)


@login_required
def ranking(request, pk):
    if request.method == 'POST':
        topic = get_object_or_404(Reaction, pk=pk)
        if not topic == topic.topic:
            return redirect('reactions:ranking', topic.topic)

        score_by_actor = User.objects.filter(reaction__topic=topic) \
            .annotate(score=Sum('reaction__score')) \
            .order_by('-score')[:10]

        return render(request, 'reactions/ranking.html', {
            'score_by_actor': score_by_actor,
        })
    raise Http404()


@login_required
def rating_good(request, pk):
    if request.method == 'POST':
        reaction = get_object_or_404(Reaction, pk=pk)
        topic = reaction.topic
        try:
            rating = Rating.objects.get(user=request.user, reaction=reaction)
            if rating.rating == 'P':
                rating.rating = 'G'
                rating.save()
                calculate_score()
        except ObjectDoesNotExist:
            Rating.objects.create(user=request.user, topic=topic, reaction=reaction, rating='G')
            calculate_score()
        return redirect('reactions:detail', pk)
    raise Http404()


@login_required
def rating_pass(request, pk):
    if request.method == 'POST':
        reaction = get_object_or_404(Reaction, pk=pk)
        topic = reaction.topic
        try:
            rating = Rating.objects.get(user=request.user, reaction=reaction)
            if rating.rating == 'G':
                rating.rating = 'P'
                rating.save()
                calculate_score()
        except ObjectDoesNotExist:
            Rating.objects.create(user=request.user, topic=topic, reaction=reaction, rating='P')
            calculate_score()
        return redirect('reactions:detail', pk)
    raise Http404()


@login_required
def reaction_new(request, pk):
    if request.method == 'POST':
        form = ReactionForm(request.POST)
        if form.is_valid():
            target = get_object_or_404(Reaction, pk=pk)
            get_object_or_404(Rating, user=request.user, reaction=pk)
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
