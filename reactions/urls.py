from django.conf.urls import url
from .views import *

app_name = 'reactions'

urlpatterns = [
    url(r'^(?P<pk>\d+)$', detail, name='detail'),
    url(r'^(?P<pk>\d+)/$', detail_s, name='detail_s'),
    url(r'^(?P<pk>\d+)/ranking$', ranking, name='ranking'),
    url(r'^(?P<pk>\d+)/good$', rate_good, name='good'),
    url(r'^(?P<pk>\d+)/pass$', rate_pass, name='pass'),
    # url(r'^(?P<pk>\d+)/delete$', delete, name='delete'),
    url(r'^(?P<pk>\d+)/reaction/new$', reaction_new, name='reaction_new'),
]
