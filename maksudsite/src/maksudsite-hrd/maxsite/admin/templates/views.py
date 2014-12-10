from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from maxsite.admin.forms import TemplateForm
from maxsite.models import AppTemplate

def index(request):
    form = TemplateForm()
    templates = AppTemplate.objects.all()
    response_dictionary = {"contact": {"pagename": "Template", "h_template":"active"}, 'form': form, 'templates': templates}
    return render_to_response('myadmin/template-admin.html', response_dictionary, context_instance=RequestContext(request))

def update(request):
    if request.method == "POST":
        form = TemplateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            id = cd["id"]
            if id:
                template = AppTemplate.objects.filter(id=long(id))[0]
            else:
                template = AppTemplate()
            
#            template.module = cd['module']
            template.name = cd['name']
            template.content = cd['content']
#            template.pagename = cd['pagename']
#            template.caption = cd['caption']

            template.save()

            return redirect ("/myadmin/templates")
    else:
        id = request.GET.get('id')
        if id:
            template = AppTemplate.objects.filter(id=long(id))[0]
            data = {'id': id,
#                'module': template.module,
#                'view': template.view,
                'name': template.name,
#                'caption': template.caption,
                'content': template.content}
            form = TemplateForm(data)
            
    response_dictionary = {"contact": {"pagename": "Template", "h_template":"active"}, 'form': form}
    return render_to_response('myadmin/template-admin.html', response_dictionary, context_instance=RequestContext(request))

