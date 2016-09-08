from django.conf import settings
from django.db import models


class Reaction(models.Model):
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True)
    topic = models.ForeignKey('self', null=True, db_index=True, related_name='topic_reactions')
    target = models.ForeignKey('self', null=True, db_index=True, related_name='target_reactions')
    contents = models.TextField(db_index=True)
    good_score = models.PositiveIntegerField(db_index=True)
    pass_score = models.PositiveIntegerField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class Rate(models.Model):
    rator = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True)
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
        unique_together = ('rator', 'reaction')

    def __str__(self):
        return str(self.id)
