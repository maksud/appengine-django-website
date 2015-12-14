from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^/create$', 'maxsite.admin.templates.views.index', name='admin_templates_create'),
    url(r'^/delete$', 'maxsite.admin.templates.views.index', name='admin_templates_delete'),
    url(r'^/update$', 'maxsite.admin.templates.views.update', name='admin_templates_update'),
    url(r'^/$', 'maxsite.admin.templates.views.index', name='admin_templates'),
)