from django.conf import settings
from django.db import models
from django.db.models import Sum
from languages import trans as _


class Reaction(models.Model):
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True)
    topic = models.ForeignKey('self', null=True, blank=True, db_index=True, related_name='topic_reactions')
    target = models.ForeignKey('self', null=True, blank=True, db_index=True, related_name='target_reactions')
    title = models.CharField(max_length=100, db_index=True, verbose_name=_('title'))
    contents = models.TextField(max_length=65535, verbose_name=_('contents'))
    url = models.CharField(max_length=100, null=True, blank=True)
    url_title = models.CharField(max_length=100, null=True, blank=True)
    url_description = models.CharField(max_length=255, null=True, blank=True)
    url_image = models.CharField(max_length=100, null=True, blank=True)
    score = models.PositiveIntegerField(default=0, db_index=True, verbose_name=_('score'))
    deleted = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    def topic_score(self):
        result = Reaction.objects.filter(topic=self.topic).aggregate(Sum('score'))['score__sum']
        return result

    def get_tree(self):
        reaction_tree = []
        reaction_tree.append(self)
        for reaction in reaction_tree:
            if reaction.target is not None:
                reaction = reaction.target
                reaction_tree.append(reaction)
        return reaction_tree

    def get_current_generation(self):
        if self.target is not None:
            return self.target.target_reactions.all()
        else:
            return Reaction.objects.filter(pk=self.pk)

    def get_previous_generation(self):
        if self.target is not None:
            return self.target.get_current_generation()
        else:
            return None

    def get_next_generation(self):
        return self.target_reactions.all()

    def get_family(self):
        return Reaction.objects.filter(topic=self.topic)


class Rating(models.Model):
    rater = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True, related_name='ratings_as_rater')
    ratee = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True, related_name='ratings_as_ratee')
    topic = models.ForeignKey(Reaction, db_index=True, related_name='topic_ratings')
    reaction = models.ForeignKey(Reaction, db_index=True, related_name='reaction_ratings')
    RATING_CHOICES = (
        ('G', 'Good'),
        ('P', 'Pass'),
    )
    rating = models.CharField(max_length=1, choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('rater', 'reaction')

    def __str__(self):
        return str(self.id)
