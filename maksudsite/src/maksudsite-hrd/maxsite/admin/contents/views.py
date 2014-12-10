from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from maxsite.admin.forms import ContentsForm
from maxsite.models import AppContent

def index(request):
    form = ContentsForm()
    contents = AppContent.objects.all()
    response_dictionary = {"contact": {"pagename": "Template", "h_template":"active"}, 'form': form, 'tiles': contents}
    return render_to_response('myadmin/content-admin.html', response_dictionary, context_instance=RequestContext(request))

def update(request):
    if request.method == "POST":
        form = ContentsForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            id = cd["id"]
            if id:
                contents = AppContent.objects.filter(id=long(id))[0]
            else:
                contents = AppContent()

            contents.name = cd['name']
            contents.language = cd['language']
            contents.content = cd['content']
            contents.url = cd['url']
            contents.caption = cd['caption']

            contents.save()

            return redirect ("/myadmin/contents")
    else:
        id = request.GET.get('id')
        if id:
            contents = AppContent.objects.filter(id=long(id))[0]
            data = {'id': id,
                'name': contents.name,
                'language': contents.language,
                'url': contents.url,
                'content': contents.content,
                'caption': contents.caption
                }
            form = ContentsForm(data)

    response_dictionary = {"contact": {"pagename": "Template", "h_template":"active"}, 'form': form, 'tiles': AppContent.objects.all()}
    return render_to_response('myadmin/content-admin.html', response_dictionary, context_instance=RequestContext(request))

def delete(request):
    return redirect ("#")