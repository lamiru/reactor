from django.conf.urls import url
from .views import *

app_name = 'topics'

urlpatterns = [
    url(r'^$', index, name='index'),
]
