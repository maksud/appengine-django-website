from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from maxsite.conferences.forms import ConferenceImportForm, ConferenceForm, ConferenceCategoryForm
from maxsite.models import Conference, ConferenceCategory, get_messages
from xlrd import open_workbook
from google.appengine.api import users
from google.appengine.api import mail
from datetime import date


def categories(request):
    if users.is_current_user_admin():
        view_url = reverse('maxsite.conferences.views.categories')
        if request.method == "POST":
            form = ConferenceCategoryForm(request.POST)
            id = form.data["id"]
            if id:
                conf = ConferenceCategory.objects.filter(id=id)[0]
            else:
                conf = ConferenceCategory()
            conf.fill_from_form(form.data)
            conf.save()
            return HttpResponseRedirect(str(view_url) + "?id=" + str(id))
        else:        
            id = request.GET.get('id')
            if id:
                conf = ConferenceCategory.objects.filter(id=id)[0]
                data = {'id': id,
                    'name': conf.name,
                    'full_name': conf.full_name,
                    'details': conf.details,
                    }
                form = ConferenceCategoryForm(data)
            else:
                form = ConferenceCategoryForm()

            categories = ConferenceCategory.objects.all()
            response_dictionary = {
                "contents"  :   {   "pagename":         "Contact Me", 
                                                "h_conferences":    "active", 
                                                "year": date.today().year}, 
                'form': form,
                'logged': True,
                'confs' : categories }
            return render_to_response('me/conference-categories.html', response_dictionary, context_instance=RequestContext(request))
    else:
        view_url = reverse('maxsite.conferences.views.index')
        return HttpResponseRedirect(view_url)

def view(request):
    id = request.GET.get('id')
    if id:
        conf = Conference.objects.filter(id=id)[0]
        response_dictionary = {
            "contents"  :   {   "pagename":         "Contact Me", 
                                            "h_conferences":    "active", 
                                            "year": date.today().year}, 
            'form': None, 
            'conf' : conf }
        return render_to_response('me/conferences-info.html', response_dictionary, context_instance=RequestContext(request))
    else:
        raise Http404("Content Not Found")

def update(request):
    user = users.get_current_user()
    if users.is_current_user_admin():
        view_url = reverse('maxsite.conferences.views.update')
        if request.method == "POST":
            form = ConferenceForm(request.POST)
            id = form.data["id"]
            if id:
                conf = Conference.objects.filter(id=id)[0]
            else:
                conf = Conference()
            conf.fill_from_form(form.data)
            conf.save()
            return HttpResponseRedirect(str(view_url) + "?id=" + str(id))
        else:        
            id = request.GET.get('id')
            if id:
                conf = Conference.objects.filter(id=id)[0]
                data = {'id': id,
                    'name': conf.name,
                    'long_name': conf.long_name,
                    'serial': conf.serial,
                    'rank_1': conf.rank_1,
                    'rank_2': conf.rank_2,
                    'rank_3': conf.rank_3,
                    'rank_4': conf.rank_4,
                    'category':  conf.category,
                    'website': conf.website,
                    'location': conf.location,
                    'is_favorite': conf.is_favorite,
                    'deadline': conf.deadline,
                    'acceptance_rate': conf.acceptance_rate,
                    'comment': conf.comment
                    }
                form = ConferenceForm(data)
            else:
                form = ConferenceForm()


            response_dictionary = {
                "contents"  :   {   "pagename":         "Contact Me", 
                                                "h_conferences":    "active", 
                                                "year": date.today().year}, 
                'form': form,
                'logged': True,
                'confs' : None }
            return render_to_response('me/conferences-update.html', response_dictionary, context_instance=RequestContext(request))
    else:
        view_url = reverse('maxsite.conferences.views.index')
        return HttpResponseRedirect(view_url)

def index(request):

    user = users.get_current_user()
    logged_in = False
    if users.is_current_user_admin():
        logged_in = True
    confs = Conference.objects.all()

    response_dictionary = {
        "contents": {   "pagename":     "Contact Me", 
                                    "h_conferences":    "active", 
                                    "year": date.today().year},
                'logged': logged_in,
               'confs' : confs }
    print confs
    return render_to_response('me/conferences-list.html', response_dictionary, context_instance=RequestContext(request))

def filter(request):
    user = users.get_current_user()
    logged_in = False
    if users.is_current_user_admin():
        logged_in = True
    if request.GET.get('favorites') and request.GET.get('favorites')=="yes":
        confs = Conference.objects.filter(is_favorite=True)
    else:
        confs = Conference.objects.all()
    if request.GET.get('deadlines') and request.GET.get('deadlines')=="yes":
        confs = [item for item in confs if item.deadline is not None]
    response_dictionary = {"contents": {"pagename": "Contact Me", "h_contact":"active", "year": date.today().year},
                           'logged': logged_in,
                           'confs' : confs }
    return render_to_response('me/conferences-list.html', response_dictionary, context_instance=RequestContext(request))

def favorite(request):
    user = users.get_current_user()
    logged_in = False
    if users.is_current_user_admin():
        logged_in = True
    confs = Conference.objects.filter(is_favorite=True)
    response_dictionary = {"contents": {"pagename": "Contact Me", "h_contact":"active", "year": date.today().year},
                           'logged': logged_in,
                           'confs' : confs }
    return render_to_response('me/conferences-list.html', response_dictionary, context_instance=RequestContext(request))

def import_excel(request):
    view_url = reverse('maxsite.conferences.views.import_excel')
    if request.method == "POST":
        form = ConferenceImportForm(request.POST)
        
        aString = request.FILES['file'].read()
        workbook = open_workbook(file_contents=aString)
        sheet = workbook.sheet_by_index(0)
        
        for row in range(1, sheet.nrows):
            ln = str(sheet.cell(row, 2).value)
            
            confs = Conference.objects.filter(long_name=ln)
            if len(confs) > 0:
                conf = confs[0]
            else:
                conf = Conference()
            conf.name = str(sheet.cell(row, 1).value)
            conf.serial = int(sheet.cell(row, 0).value)
            conf.long_name = str(sheet.cell(row, 2).value)
            conf.rank_1 = str(sheet.cell(row, 3).value)            
            conf.category = str(sheet.cell(row, 5).value)
            conf.website = ""
            conf.location = ""
            conf.is_favorite = False
#             conf.deadline = ""
            conf.acceptance_rate = ""
            conf.comment = ""
            
            conf.save()
        
            
#             contact.save()
        return HttpResponseRedirect(view_url)
            
            # Mail
#             sender_address = "Website <admin@maksudsite.appspot.com>"
#             subject = "New Message Posted on your website"
#             body = """New Message Received: %s""" % cd['message']
# 
#             user_address = "maksud.buet@gmail.com"
#             mail.send_mail(sender_address, user_address, subject, body)
             
#             response_dictionary = {"contact": {"pagename": "Contact Me", "h_contact":"active"} }
#             return render_to_response('me/contact-success.html', response_dictionary, context_instance=RequestContext(request))
    else:
        form = ConferenceImportForm()

    response_dictionary = {"contents": {"pagename": "Contact Me", "h_contact":"active", "year": date.today().year}, 'form': form  }
    return render_to_response('me/conferences-import.html', response_dictionary, context_instance=RequestContext(request))

#     render(request, 'me/conference.html', {'form': ConferenceForm()})   


