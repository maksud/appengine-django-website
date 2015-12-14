from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^/delete/$', 'maxsite.admin.blobstoredocuments.views.delete', name='admin_documents_delete'),
    url(r'^/update/$', 'maxsite.admin.blobstoredocuments.views.update', name='admin_documents_update'),
#    url(r'^/upload/$', 'maxsite.admin.documents.views.upload', name='admin_documents_upload'),
#    url(r'^/download/$', 'maxsite.admin.documents.views.download', name='admin_documents_download'),
    url(r'^/$', 'maxsite.admin.blobstoredocuments.views.index', name='admin_documents'),
)