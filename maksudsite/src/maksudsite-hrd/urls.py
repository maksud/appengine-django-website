from apps import search
from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.auth.forms import AuthenticationForm
from maxsite.models import AppContent, AppTemplate, AppDocument, AppMessage, \
    AppModule, AppView, AppTextFile, Publication, Conference, ConferenceCategory, News

admin.site.register(AppContent)
admin.site.register(AppTemplate)
admin.site.register(AppDocument)
admin.site.register(AppMessage)
admin.site.register(AppModule)
admin.site.register(AppView)
admin.site.register(AppTextFile)
admin.site.register(Publication)
admin.site.register(Conference)
admin.site.register(ConferenceCategory)
admin.site.register(News)


search.autodiscover()
admin.autodiscover()

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    # Uncomment this for admin:
    (r'^admin/', include(admin.site.urls)),
    url(r'^dynafile/(?P<name>.{0,50})/$', "maxsite.admin.dynafile.views.dynafile", name="url_dynafile"),
#    (r'^document/(?P<filename>.{1,50})$', "maxsite.admin.documents.views.download"),
    (r'^document/(?P<filename>.{1,50})$', "maxsite.admin.blobstoredocuments.views.download"),
    (r'^myadmin', include('maxsite.admin.urls')),
    (r'^contact', include('maxsite.contact.urls')),
    (r'^publications', include('maxsite.publications.urls')),
    (r'^news', include('maxsite.news.urls')),
    (r'^conferences', include('maxsite.conferences.urls')),
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/images/favicon.ico'}),
    url(r'^(?P<module>\w{1,50})/(?P<view>\w{1,50})/$', "maxsite.index.views.module_view_index"),
    url(r'^(?P<module>\w{1,50})/$', "maxsite.index.views.module_index"),
    (r'^', include('maxsite.index.urls')),
)
