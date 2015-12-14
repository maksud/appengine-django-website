from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from maxsite.publications.forms import PublicationForm
from maxsite.models import Publication, PUBLICATION_CHOICES
from xlrd import open_workbook
from google.appengine.api import users
from google.appengine.api import mail
from datetime import date

def update(request):
    user = users.get_current_user()
    if users.is_current_user_admin():
        view_url = reverse('maxsite.publications.views.update')
        if request.method == "POST":
            form = PublicationForm(request.POST)
            id = form.data["id"]
            if id:
                conf = Publication.objects.filter(id=id)[0]
            else:
                conf = Publication()
            conf.fill_from_form(form.data)
            conf.save()
            return HttpResponseRedirect(str(view_url) + "?id=" + str(id))
        else:        
            id = request.GET.get('id')
            if id:
                data = Publication.objects.filter(id=id)[0]
                form = PublicationForm(instance=data)
            else:
                form = PublicationForm()
            response_dictionary = {"contents": {"pagename": "Publications", "h_publications":"active", "year": date.today().year}, 'form': form, 'confs' : None }
            return render_to_response('me/publications-update.html', response_dictionary, context_instance=RequestContext(request))
    else:
        view_url = reverse('maxsite.publicatios.views.index')
        return HttpResponseRedirect(view_url)

def index(request):
    user = users.get_current_user()
    
    logged_in = False
    if users.is_current_user_admin():
        logged_in = True

    allpapers  = Publication.objects.all().order_by("pub_type", "-serial")

    serials ={}
    for k in PUBLICATION_CHOICES:
        serials[k[0]]=1
    

    for paper in allpapers:
        paper.sequence = serials[paper.pub_type]
        serials[paper.pub_type] = serials[paper.pub_type] + 1
        paper.pub_type = paper.pub_type[2:]
        seq = float(paper.year)
        if paper.serial > 0:
            seq = seq + paper.serial/1000.0
        else:
            seq = seq + 0.9999
        paper.seq = seq
    response_dictionary = {"contents": {"pagename": "Publications", "h_publications":"active", "year": date.today().year},
            'logged': logged_in,
            'allpapers': allpapers }
    return render_to_response('me/publications-list.html', response_dictionary, context_instance=RequestContext(request))
