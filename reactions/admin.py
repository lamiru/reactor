from django.contrib import admin
from .models import *


class ReactionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'actor', 'topic', 'target',
        'contents', 'score', 'deleted',
        'created_at', 'updated_at',
    )

admin.site.register(Reaction, ReactionAdmin)


class RateAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'topic', 'reaction', 'rate',
        'created_at', 'updated_at',
    )

admin.site.register(Rate, RateAdmin)
