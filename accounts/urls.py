from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth.views import logout
from .views import *

app_name = 'accounts'

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', logout, {'next_page': 'accounts:login'}, name='logout'),
    url(r'^profile/$', profile, name='profile'),
    url(r'^$', index, name='index'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
