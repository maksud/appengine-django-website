from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Template
from django.template.context import Context
from maxsite.models import get_view, get_content_by_tile,\
    get_content_string_by_tile, get_content_model_by_tile
import logging
from datetime import date
from django.contrib.auth.models import User
from google.appengine.api import users

import os


def response_from_db_or_default(request, module, view, pagename, active_key=None):
#     create_admin()
    user = users.get_current_user()

    loginurl = None
    logouturl = None
    if not user:
        loginurl = users.create_login_url(request.get_full_path())
    else:
        logouturl = users.create_logout_url(request.get_full_path())

    response_dictionary = {"contents": {"pagename": pagename, "module": module, "view": view, "title": ""}}
    appview = get_view(module, view)

    if appview:
        if appview.is_redirect:
            return HttpResponseRedirect(appview.url)
        
        response_dictionary["contents"]["title"] = appview.caption
        active_key = module
        response_dictionary["contents"]["h_%s" % active_key] = "active" 

        if hasattr(appview, 'default_content') and appview.default_content:
            content_model = appview.default_content
            content_id = appview.default_content.id
        else:
            content_model, content_id = get_content_model_by_tile(module + "-" + view)
    
        if users.is_current_user_admin():
            response_dictionary["contents"]["edit"] = True
            response_dictionary["contents"]["cid"] = content_id
            response_dictionary["contents"]["path"] = request.path_info
        else:
            response_dictionary["contents"]["edit"] = False

        response_dictionary["contents"]["loginurl"] = loginurl
        response_dictionary["contents"]["logouturl"] = logouturl
        response_dictionary["contents"]["content"] = content_model.content
        response_dictionary["contents"]["css"] = content_model.css
        response_dictionary["contents"]["js"] = content_model.js
        response_dictionary["contents"]["year"] = date.today().year
        response_dictionary["contents"]["current_url"] = request.get_full_path()
        
        if hasattr(appview, 'template') and appview.template:
            return response_from_string(appview.template.content, response_dictionary)
        else:        
            return render_to_response('layout/default.html', response_dictionary)
    else:
        if users.is_current_user_admin():
#             No View Found, Create View!!
            pass
        else:
            raise Http404("Page Not Available")
#        logging.info("@@@@@ AppView NOT Found")
#        content = get_content_by_tile(module + "-" + view)
#        if content:
#            response_dictionary["contents"]["content"] = content.content
#            response_dictionary["contents"]["pagename"] = content.caption
#            response_dictionary["contents"]["title"] = content.caption
#            return render_to_response('layout/default.html', response_dictionary)
#        else:
#        raise Http404("Content Not Found")
#        return HttpResponse(status=404)

try:
    from django.views.decorators.csrf import csrf_exempt
except ImportError:
    def csrf_exempt(func):
        return func

def render_from_string(template, dictionary=None, context_instance=None):
    t = Template(template)

    if context_instance:
        context_instance.update(dictionary)
    else:
        context_instance = Context(dictionary)
    return t.render(context_instance)

def response_from_string(*template, **kwargs):
    httpresponse_kwargs = {'mimetype': kwargs.pop('mimetype', None)}
    return HttpResponse(render_from_string(*template, **kwargs), **httpresponse_kwargs)