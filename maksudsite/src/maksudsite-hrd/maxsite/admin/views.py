from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from google.appengine.api import memcache
from google.appengine.api.app_logging import logging
import logging

from django.contrib.auth.models import User
from google.appengine.api import users

from datetime import datetime, date
from google.appengine.api import search


try:
    from django.views.decorators.csrf import csrf_exempt
except ImportError:
    def csrf_exempt(func):
        return func

def create_admin():
    try:
        u = User.objects.get(username='admin')
        u.set_password('123456')
        u.save()
    except:
        user = User.objects.create_superuser('admin', 'admin@maksudsite.com', '123456')
#     userlist = User.objects.all()
#     print "Number of Users", len(userlist)
#     for u in userlist:
#         print "Username", u.username, u.password
#     if len(userlist) == 0:
#     user = User.objects.create_user('admin', 'admin@maksudsite.com', '123456')        
    pass


def create_search_index():
    my_document = search.Document(
    # Setting the doc_id is optional. If omitted, the search service will create an identifier.
    doc_id='PA6-5000',
    fields=[
       search.TextField(name='customer', value='Joe Jackson'),
       search.HtmlField(name='comment', value='this is <em>marked up</em> text'),
       search.NumberField(name='number_of_visits', value=7),
       search.DateField(name='last_visit', value=datetime.now()),
       search.DateField(name='birthday', value=datetime(year=1960, month=6, day=19)),
       search.GeoField(name='home_location', value=search.GeoPoint(37.619, -122.37))
       ])
    
    try:
        index = search.Index(name="myIndex")
        index.put(my_document)
    except search.Error:
        logging.exception('Put failed')

def dashboard(request, name=None):
    redirect_url = request.GET["p"]
#     print "In Dashboard"
#     return
    if name == "flush_all":
        memcache.flush_all()
        logging.info("Memcache is Flushed")
    elif name == "reset_django":
        create_admin()
        logging.info("Password is Reset")
        pass
    elif name == "index_documents":
        create_search_index()
        pass
    return redirect(redirect_url)
#     return redirect ("/myadmin")
#     return render_to_response('myadmin/index.html', response_dictionary, context_instance=RequestContext(request))


def index(request, name=None):
    cache_stats = memcache.get_stats()
    response_dictionary = {"contents": {"pagename": "Admin Dashboard", "year": date.today().year}, 'stats': cache_stats}
    return render_to_response('myadmin/index.html', response_dictionary, context_instance=RequestContext(request))
