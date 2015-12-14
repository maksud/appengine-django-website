from django.shortcuts import render_to_response
from django.template import RequestContext
from maxsite.contact.forms import ContactForm
from maxsite.models import AppMessage, get_messages
from datetime import date
from google.appengine.api import mail
from maxsite.helper import response_from_db_or_default
from maxsite.models import get_view


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
            
            #Mail
            sender_address = "contact@maksudsite.appspotmail.com"
            subject = "New Message Posted on your website"
            body = """New Message Received: %s""" % cd['message']

            user_address = "maksud.buet@gmail.com"
            mail.send_mail(sender_address, user_address, subject, body)
             
            response_dictionary = {"contact": {"pagename": "Contact Me", "h_contact":"active", "year": date.today().year} }
            return render_to_response('me/contact-success.html', response_dictionary, context_instance=RequestContext(request))
    else:
        contacts = get_messages()
        form = ContactForm()

    contactinfo_view = get_view("home", "contactinfo")

    response_dictionary = {"contents": {"pagename": "Contact Me", "h_contact":"active", "year": date.today().year},  'form': form, 'messages' : contacts, 'contactinfo': contactinfo_view.default_content.content  }
    return render_to_response('me/contact.html', response_dictionary, context_instance=RequestContext(request))   


