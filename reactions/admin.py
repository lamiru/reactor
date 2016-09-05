from django.contrib import admin
from .models import *


class ReactionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'actor', 'topic', 'target',
        'contents', 'good_score', 'pass_score',
        'created_at', 'updated_at',
    )

admin.site.register(Reaction, ReactionAdmin)
