from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from maxsite.news.forms import NewsForm
from maxsite.models import News
from xlrd import open_workbook
from google.appengine.api import users
from google.appengine.api import mail
from datetime import date

def update(request):
    user = users.get_current_user()
    if users.is_current_user_admin():
        view_url = reverse('maxsite.news.views.update')
        if request.method == "POST":
            form = NewsForm(request.POST)
            id = form.data["id"]
            if id:
                entry = News.objects.filter(id=id)[0]
            else:
                entry = News()
            entry.fill_from_form(form.data)
            entry.save()
            return HttpResponseRedirect(str(view_url) + "?id=" + str(id))
        else:        
            id = request.GET.get('id')
            if id:
                entry = News.objects.filter(id=id)[0]
                data = {'id': id,
                    "content": entry.content,
                    "title": entry.title,
                    "when": entry.when,
                    "kind": entry.kind
                    }
                form = NewsForm(data)
            else:
                form = NewsForm()
            response_dictionary = {"contents": {"pagename": "News", "h_news":"active", "year": date.today().year}, 'form': form, 'confs' : None }
            return render_to_response('me/news-update.html', response_dictionary, context_instance=RequestContext(request))
    else:
        view_url = reverse('maxsite.news.views.index')
        return HttpResponseRedirect(view_url)

def index(request):
    user = users.get_current_user()
    
    logged_in = False
    if users.is_current_user_admin():
        logged_in = True

    allnews  = News.objects.all().order_by("-when")
    response_dictionary = {"contents": {"pagename": "News", "h_news":"active",  "year": date.today().year},
            'logged': logged_in,
            'allnews':allnews }
    return render_to_response('me/news-timeline.html', response_dictionary, context_instance=RequestContext(request))
