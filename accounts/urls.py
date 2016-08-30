from django.conf.urls import url
from django.contrib.auth.views import logout
from .views import *

app_name = 'accounts'

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', logout, {'next_page': 'accounts:login'}, name='logout'),
    url(r'^$', index, name='index'),
]
