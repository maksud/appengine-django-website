from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^/delete$', 'maxsite.admin.contents.views.delete', name='admin_contents_delete'),
    url(r'^/update$', 'maxsite.admin.contents.views.update', name='admin_contents_update'),
    url(r'^/$', 'maxsite.admin.contents.views.index', name='admin_contents'),
)