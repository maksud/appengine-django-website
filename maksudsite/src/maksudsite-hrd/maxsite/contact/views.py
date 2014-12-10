from django.shortcuts import render_to_response
from django.template import RequestContext
from maxsite.contact.forms import ContactForm
from maxsite.models import AppMessage, get_messages

def contact(request):
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
            
            response_dictionary = {"contact": {"pagename": "Contact Me", "h_contact":"active"} }
            return render_to_response('me/contact-success.html', response_dictionary, context_instance=RequestContext(request))
    else:
        contacts = get_messages()
        form = ContactForm()

    response_dictionary = {"contents": {"pagename": "Contact Me", "h_contact":"active"},  'form': form, 'messages' : contacts }
    return render_to_response('me/contact.html', response_dictionary, context_instance=RequestContext(request))   


