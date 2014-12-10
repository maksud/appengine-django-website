from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from google.appengine.api import memcache
from google.appengine.api.app_logging import logging
import logging


try:
    from django.views.decorators.csrf import csrf_exempt
except ImportError:
    def csrf_exempt(func):
        return func

def dashboard(request, name=None):
    redirect_url = request.GET["p"]
#     print "SSS"
#     return
    if name == "flush_all":
        memcache.flush_all()
        logging.info("Memcache is Flushed")
    return redirect(redirect_url)
#     return redirect ("/myadmin")
#     return render_to_response('myadmin/index.html', response_dictionary, context_instance=RequestContext(request))


def index(request, name=None):
    cache_stats = memcache.get_stats()
    response_dictionary = {"contact": {"pagename": "Admin Dashboard",}, 'stats': cache_stats}
    return render_to_response('myadmin/index.html', response_dictionary, context_instance=RequestContext(request))