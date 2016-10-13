from django.conf import settings
from django.db import models


class Reaction(models.Model):
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True)
    topic = models.ForeignKey('self', null=True, blank=True, db_index=True, related_name='topic_reactions')
    target = models.ForeignKey('self', null=True, blank=True, db_index=True, related_name='target_reactions')
    title = models.CharField(max_length=100, db_index=True)
    contents = models.TextField(db_index=True)
    score = models.PositiveIntegerField(db_index=True)
    deleted = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    def get_tree(self):
        reaction_tree = []
        reaction_tree.append(self)
        for reaction in reaction_tree:
            if reaction.target is not None:
                reaction = reaction.target
                reaction_tree.append(reaction)
        return reaction_tree

    def get_brothers(self):
        if self.target is not None:
            return self.target.target_reactions.all()
        else:
            return Reaction.objects.filter(target=None)

    def get_parents(self):
        if self.target is not None:
            return self.target.get_brothers()
        else:
            return None

    def get_children(self):
        return self.target_reactions.all()

    def get_family(self):
        return Reaction.objects.filter(topic=self.topic)


class Rate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True)
    topic = models.ForeignKey(Reaction, db_index=True, related_name='topic_rates')
    reaction = models.ForeignKey(Reaction, db_index=True, related_name='reaction_rates')
    RATE_CHOICES = (
        ('G', 'Good'),
        ('P', 'Pass'),
    )
    rate = models.CharField(max_length=1, choices=RATE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'reaction')

    def __str__(self):
        return str(self.id)
