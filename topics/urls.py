from django.conf.urls import url
from .views import *

app_name = 'topics'

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^new/$', new, name='new'),
    url(r'^(?P<pk>\d+)/delete$', delete, name='delete'),
]
