from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^/create$', 'maxsite.admin.messages.views.index', name='admin_messages_create'),
    url(r'^/delete$', 'maxsite.admin.messages.views.delete', name='admin_messages_delete'),
    url(r'^/approve$', 'maxsite.admin.messages.views.approve', name='admin_messages_approve'),
    url(r'^/$', 'maxsite.admin.messages.views.index', name='admin_messages'),
)