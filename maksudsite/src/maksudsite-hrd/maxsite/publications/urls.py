from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^/update/$', 'maxsite.publications.views.update', name='publications_update'),
    url(r'^/$', 'maxsite.publications.views.index', name='publications_index'),
)
