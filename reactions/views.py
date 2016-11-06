from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Sum
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from helpers.score import calculate_score, calculate_topic_score
from .forms import *
from .models import *
from accounts.models import Notification


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
        rating = Rating.objects.get(rater=request.user, reaction=current_reaction).rating
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
def recent(request, pk):
    if request.method == 'POST':
        reaction_list = get_list_or_404(Reaction.objects.order_by('-id'), topic=pk)

        return render(request, 'reactions/recent.html', {
            'reaction_list': reaction_list,
        })
    raise Http404()


@login_required
def ranking(request, pk):
    if request.method == 'POST':
        topic = get_object_or_404(Reaction, pk=pk)

        score_by_actor = User.objects.filter(reaction__topic=topic) \
            .annotate(score=Sum('reaction__score')) \
            .order_by('-score')[:10]

        return render(request, 'reactions/ranking.html', {
            'score_by_actor': score_by_actor,
        })
    raise Http404()


@login_required
def scrapbook(request, pk):
    if request.method == 'POST':
        scrapbook_list = Reaction.objects.filter(topic=pk).exclude(url='').order_by('-score')

        return render(request, 'reactions/scrapbook.html', {
            'scrapbook_list': scrapbook_list,
        })
    raise Http404()


@login_required
def rating_good(request, pk):
    if request.method == 'POST':
        reaction = get_object_or_404(Reaction, pk=pk)
        topic = reaction.topic
        try:
            rating = Rating.objects.get(rater=request.user, reaction=reaction)
            if rating.rating == 'P':
                rating.rating = 'G'
                rating.save()
                calculate_score(reaction)
                calculate_topic_score(topic)
        except ObjectDoesNotExist:
            rating = Rating.objects.create(rater=request.user, ratee=reaction.actor, topic=topic, reaction=reaction, rating='G')
            if request.user != reaction.actor:
                Notification.objects.create(
                    user=reaction.actor, active_user=request.user, passive_user=reaction.actor,
                    reaction=reaction, rating=rating, category='RA',
                )
            calculate_score(reaction)
            calculate_topic_score(topic)
        return redirect('reactions:detail', pk)
    raise Http404()


@login_required
def rating_pass(request, pk):
    if request.method == 'POST':
        reaction = get_object_or_404(Reaction, pk=pk)
        topic = reaction.topic
        try:
            rating = Rating.objects.get(rater=request.user, reaction=reaction)
            if rating.rating == 'G':
                rating.rating = 'P'
                rating.save()
                calculate_score(reaction)
                calculate_topic_score(topic)
        except ObjectDoesNotExist:
            rating = Rating.objects.create(rater=request.user, ratee=reaction.actor, topic=topic, reaction=reaction, rating='P')
            if request.user != reaction.actor:
                Notification.objects.create(
                    user=reaction.actor, active_user=request.user, passive_user=reaction.actor,
                    reaction=reaction, rating=rating, category='RA',
                )
            calculate_score(reaction)
            calculate_topic_score(topic)
        return redirect('reactions:detail', pk)
    raise Http404()


@login_required
def reaction_new(request, pk):
    if request.method == 'POST':
        form = ReactionForm(request.POST)
        if form.is_valid():
            #--- Create a reaction ---#
            target = get_object_or_404(Reaction, pk=pk)
            get_object_or_404(Rating, rater=request.user, reaction=pk) # Confirm that the request user made rating to the target.
            reaction = form.save(commit=False)
            reaction.actor = request.user
            reaction.target = target
            reaction.topic = target.topic
            reaction.save()

            #--- Create a notification ---#
            if request.user != target.actor:
                Notification.objects.create(
                    user=target.actor, active_user=request.user, passive_user=target.actor,
                    category='RE', reaction=reaction,
                )

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
