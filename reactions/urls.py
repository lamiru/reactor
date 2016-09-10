from django.conf.urls import url
from .views import *

app_name = 'reactions'

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', detail, name='detail'),
]
