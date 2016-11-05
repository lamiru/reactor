from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import *


UserAdmin.list_display = (
    'id', 'username', 'email', 'first_name', 'last_name',
    'is_active', 'is_staff', 'is_superuser', 'date_joined',
)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'photo', 'about',
        'created_at', 'updated_at',
    )

admin.site.register(UserProfile, UserProfileAdmin)


class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'active_user', 'passive_user',
        'category', 'reaction', 'rating', 'checked',
        'created_at', 'updated_at',
    )

admin.site.register(Notification, NotificationAdmin)
