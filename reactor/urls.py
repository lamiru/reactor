from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = i18n_patterns(
    url(r'^admin', admin.site.urls),
    url(r'^', include('accounts.urls')),
    url(r'^reactions', include('reactions.urls')),
    url(r'^topics', include('topics.urls')),
    prefix_default_language=False
)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
