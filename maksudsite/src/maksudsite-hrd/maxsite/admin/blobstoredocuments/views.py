from apps.filetransfers.api import prepare_upload
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.views.generic.simple import direct_to_template
from google.appengine.ext import blobstore
from maxsite.admin.documents.forms import DocumentUploadForm
from maxsite.blobstore_helper import get_uploads, send_blob
from maxsite.models import AppDocument
from datetime import date
import logging
import urllib

def index(request):
    view_url = reverse('maxsite.admin.blobstoredocuments.views.index')
    if request.method == 'POST':
        document_blobs = get_uploads(request, field_name="document", populate_post=True)
        form = DocumentUploadForm(request.POST)
        if form.is_valid() and len(document_blobs) == 1:
            id = form.cleaned_data["id"]
            if id:
                document = AppDocument.objects.filter(id=id)[0]
            else:
                document = AppDocument()
            document.fill_from_form(form.cleaned_data, document_blobs[0])
            # document.fill_from_form(form.cleaned_data, blobstore)
            document.save()

            return HttpResponseRedirect(view_url)
        return HttpResponseRedirect(view_url)
    elif request.session.has_key('upload_form_post'):
        form = DocumentUploadForm(request.session['upload_form_post'])
    else:
        form = DocumentUploadForm()

    response_dictionary = {"contents": {"pagename": "Documents", "h_documents":"active", "year": date.today().year}, 'url_action': blobstore.create_upload_url(view_url), 'form': form, 'documents': AppDocument.objects.all()}
    return render_to_response('myadmin/document-admin.html', response_dictionary, context_instance=RequestContext(request))

def update(request):
    update_url = reverse('maxsite.admin.blobstoredocuments.views.update')
    if request.method == 'POST':
        document_blobs = get_uploads(request, field_name="document", populate_post=True)
        form = DocumentUploadForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data["id"]
            if id:
                document = AppDocument.objects.filter(id=id)[0]
            else:
                document = AppDocument()

            if len(document_blobs) == 1:
                document.fill_from_form(form.cleaned_data, document_blobs[0])
            else:
                document.fill_from_form(form.cleaned_data)
            document.save()
            return HttpResponseRedirect(update_url)
        else:
            id = request.GET.get('id')
            if id:
                document = AppDocument.objects.filter(id=id)[0]
                data = {'id': id,
                    'name': document.name,
                    'title': document.title,
                    }
                form = DocumentUploadForm(data)        
            #return HttpResponseRedirect(view_url)
    elif request.session.has_key('upload_form_post'):
        form = DocumentUploadForm(request.session['upload_form_post'])
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
    response_dictionary = {"contents": {"pagename": "Documents", "h_documents":"active", "year": date.today().year}, 'url_action': blobstore.create_upload_url(update_url), 'form': form, 'documents': AppDocument.objects.all()}
    return render_to_response('myadmin/document-admin.html', response_dictionary, context_instance=RequestContext(request))

def delete(request):
    return redirect ("/myadmin/documents")

def download(request, filename):
    results = AppDocument.objects.filter(name=filename)[:1]    
    for result in results:
        blob_id_var = result.blob_key
        blob_id = str(urllib.unquote(blob_id_var))            
        # try:
            # blobinfo = AppBlobStore.get(blob_id)
            # return HttpResponse(blobinfo.content, mimetype=blobinfo.content_type)
        # except:
        blob = blobstore.BlobInfo.get(blob_id)
        return send_blob(request, blob)
    else:
        redirect ("/myadmin/documents")
    