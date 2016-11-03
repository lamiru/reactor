from django.conf.urls import url
from .views import *

app_name = 'topics'

urlpatterns = [
    url(r'^$', index, name='index'),
    # url(r'^/(?P<pk>\d+)/recent$', recent, name='recent'),
    url(r'^/search$', search, name='search'),
    url(r'^/new$', new, name='new'),
]
