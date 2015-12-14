from django.conf.urls.defaults import *

urlpatterns = patterns('',
     url(r'^/$', 'maxsite.contact.views.contact', name='me_contact'),
     # url(r'^/$', 'maxsite.conferences.views.index', name='me_contact'),
)
