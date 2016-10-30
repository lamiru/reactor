from django.contrib import admin
from .models import *


class ReactionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'actor', 'topic', 'target',
        'title', 'contents', 'url', 'score', 'deleted',
        'created_at', 'updated_at',
    )

admin.site.register(Reaction, ReactionAdmin)


class RatingAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'topic', 'reaction', 'rating',
        'created_at', 'updated_at',
    )

admin.site.register(Rating, RatingAdmin)
