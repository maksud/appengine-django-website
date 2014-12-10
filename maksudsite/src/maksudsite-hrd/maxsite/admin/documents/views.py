from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from maxsite.admin.documents.forms import DocumentUploadForm
from maxsite.models import AppDocument, AppBlobStore
import logging
import urllib

def index(request):
    view_url = reverse('maxsite.admin.documents.views.index')
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            id = form.cleaned_data["id"]
            if id:
                document = AppDocument.objects.filter(id=id)[0]
            else:
                document = AppDocument()
                
                
            if form.cleaned_data["document"]:
                blobstore = AppBlobStore()
                blobstore.fill_from_form(form.cleaned_data["document"])
                blobstore.put()
            else:
                blobstore = None

            document.fill_from_form(form.cleaned_data, blobstore)
            document.save()

            return HttpResponseRedirect(view_url)
        return HttpResponseRedirect(view_url)


    else:
        id = request.GET.get('id')
        if id:
            document = AppDocument.objects.filter(id=id)[0]
            data = {'id': id,
                'name': document.name,
                'title': document.title,
                }
            form = DocumentUploadForm(data)
        else:
            form = DocumentUploadForm()

    response_dictionary = {"contact": {"pagename": "Documents"}, 'url_action': view_url, 'form': form, 'documents': AppDocument.objects.all()}
    return render_to_response('myadmin/document-admin.html', response_dictionary, context_instance=RequestContext(request))

def delete(request):
    return redirect ("/myadmin/documents")

def download(request, filename):
    results = AppDocument.objects.filter(name=filename)[:1]    
    for result in results:
        blog_id_var = result.blob_key
        blob_id = str(urllib.unquote(blog_id_var))
#        logging.fatal(blob_id)
        blobinfo = AppBlobStore.get(blob_id)
        return HttpResponse(blobinfo.content, mimetype=blobinfo.content_type)
    else:
        redirect ("/myadmin/documents")
    