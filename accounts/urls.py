from django.conf.urls import url
from django.contrib.auth.views import logout
from .views import *

app_name = 'accounts'

urlpatterns = [
    url(r'^$', index, name='index'),
]
