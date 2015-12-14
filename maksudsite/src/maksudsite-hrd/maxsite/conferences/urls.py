from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^/view/$', 'maxsite.conferences.views.view', name='conferences_view'),
    url(r'^/update/$', 'maxsite.conferences.views.update', name='conferences_update'),
    url(r'^/import/$', 'maxsite.conferences.views.import_excel', name='conferences_import'),
    url(r'^/filter/$', 'maxsite.conferences.views.filter', name='conferences_filter'),
    url(r'^/favorite/$', 'maxsite.conferences.views.favorite', name='conferences_favorite'),
    url(r'^/categories/$', 'maxsite.conferences.views.categories', name='conferences_categories'),
    url(r'^/$', 'maxsite.conferences.views.index', name='conferences_index'),
)
