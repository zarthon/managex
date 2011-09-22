from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
# Uncomment the next two lines to enable the admin:

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('managex.udhar',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','views.index'),
    url(r'^login/','views.login'),
    url(r'^logout/','views.logout'),
    url(r'^signup/','views.register')
)

urlpatterns += patterns('',(r'^managex/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}),)
