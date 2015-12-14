from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^/contents', include('maxsite.admin.contents.urls')),
#    (r'^/documents', include('maxsite.admin.documents.urls')),
    (r'^/documents', include('maxsite.admin.blobstoredocuments.urls')),
    (r'^/dynafile', include('maxsite.admin.dynafile.urls')),
    (r'^/templates', include('maxsite.admin.templates.urls')),
    (r'^/messages', include('maxsite.admin.messages.urls')),
    (r'^/dashboard/(?P<name>.{0,50})$', 'maxsite.admin.views.dashboard'),
    url(r'^/$', 'maxsite.admin.views.index', name='admin_index'),
#     http://localhost:9080/myadmin/dashboard/flush_all
)