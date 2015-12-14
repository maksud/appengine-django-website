from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^/delete$', 'maxsite.admin.dynafile.views.delete', name='admin_dynafile_delete'),
    url(r'^/update$', 'maxsite.admin.dynafile.views.update', name='admin_dynafile_update'),
    url(r'^/upload$', 'maxsite.admin.dynafile.views.upload', name='admin_dynafile_upload'),
    url(r'^/$', 'maxsite.admin.dynafile.views.index', name='admin_dynafile'),
)