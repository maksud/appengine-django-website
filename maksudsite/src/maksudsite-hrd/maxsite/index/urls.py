from django.conf.urls.defaults import *

urlpatterns = patterns('',
       url(r'^$', 'maxsite.index.views.index', name='index_index'),
)