from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from google.appengine.ext import db
from maxsite.admin.dynafile.forms import DynaTextForm, DynaUploadForm
from maxsite.models import AppTextFile, get_static_file

def index(request):
#    contacts = StaticContent.all().fetch(100)
    contacts = AppTextFile.objects.all()
    uploadForm = DynaUploadForm()
    textForm = DynaTextForm()

    response_dictionary = {"contact": {"pagename": "Documents", "h_contact":"active"}, 'uploadForm': uploadForm, 'textForm': textForm, 'dynafiles': contacts}
    return render_to_response('myadmin/dynafile-admin.html', response_dictionary, context_instance=RequestContext(request))

def upload(request):
    if request.method == "POST":
        form = DynaUploadForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            file = cd["file"];
            
            row = AppTextFile.objects.filter(name=file.name)[:1]
            if row:
                dynafile = row[0]
            else:
                dynafile = AppTextFile()
            
            text = file.read()
            dynafile.content = text 
            dynafile.content_type = file.content_type
            dynafile.name = file.name
            dynafile.save()            
    return redirect("/myadmin/dynafile")

def dynafile(request, name):
    content = get_static_file(name)
    return HttpResponse(content.content, mimetype=content.content_type)
    


def update(request):
    if request.method == "POST":
        form = DynaTextForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            id = cd["id"]
            if id:
                dynafile = AppTextFile.objects.filter(id=long(id))[0]
            else:
                dynafile = AppTextFile()

            dynafile.name = cd['name']
            dynafile.content = cd['content']
            dynafile.content_type = cd['content_type']

            dynafile.save()

            return redirect ("/myadmin/dynafile")
    else:
        id = request.GET.get('id')
        if id:
            dynafile = AppTextFile.objects.filter(id = long(id))[0]
            data = {'id': id,
                'name': dynafile.name,
                'content_type': dynafile.content_type,
                'content': dynafile.content,
                }
            form = DynaTextForm(data)
        else:
            form = DynaTextForm()

    response_dictionary = {"contact": {"pagename": "Template", "h_dynafile":"active"},'uploadForm': DynaUploadForm(), 'textForm': form, 'dynafiles': AppTextFile.objects.all()}
    return render_to_response('myadmin/dynafile-admin.html', response_dictionary, context_instance=RequestContext(request))

def delete(request):
    return redirect ("/myadmin/dynafile/")
