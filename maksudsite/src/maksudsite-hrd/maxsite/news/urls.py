from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^/update/$', 'maxsite.news.views.update', name='news_update'),
    url(r'^/$', 'maxsite.news.views.index', name='news_index'),
)
