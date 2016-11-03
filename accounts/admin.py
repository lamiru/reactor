from django.contrib import admin
from .models import *


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'photo', 'about',
        'created_at', 'updated_at', 
    )

admin.site.register(UserProfile, UserProfileAdmin)
