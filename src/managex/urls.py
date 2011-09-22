from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
# Uncomment the next two lines to enable the admin:

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','managex.udhar.views.login')
)

urlpatterns += patterns('',(r'^managex/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}),)
