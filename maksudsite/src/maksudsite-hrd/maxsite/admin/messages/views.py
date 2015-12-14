from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from maxsite.contact.forms import ContactForm
from maxsite.models import AppMessage, get_messages
from datetime import date

def index(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        
        if form.is_valid():
            cd = form.cleaned_data
            contact = AppMessage()
            contact.name = cd['name'] 
            contact.email = cd['email'] 
            contact.message = cd['message']
            contact.website = cd['website']
            contact.ip = request.META["REMOTE_ADDR"]
            contact.accepted = False
            
            contact.save() 
    else:
        contacts = get_messages(False)
        form = ContactForm()

    response_dictionary = {"contents": {"pagename": "Contact Me", "h_messages":"active", "year": date.today().year}, 'form': form, 'messages': contacts}
    return render_to_response('myadmin/contact-admin.html', response_dictionary, context_instance=RequestContext(request))   

def approve(request):
    id = request.GET.get('id')
    if id:
        message = AppMessage.objects.get(id=long(id))
        if message:
            message.accepted = True
            message.save()

    return redirect("/myadmin/messages")

def delete(request):
    id = request.GET.get('id')
    if id:
        message = AppMessage.objects.get(id=long(id))
        if message:
            message.delete()

    return redirect("/myadmin/messages")
