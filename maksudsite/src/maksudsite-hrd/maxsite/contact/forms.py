from django import forms
from django.template.loader import render_to_string

from uni_form.helpers import FormHelper, Submit, Reset

from uni_form.helpers import Layout, Fieldset, Column, Row, HTML

class ContactForm(forms.Form):
    name = forms.CharField(label="Name", max_length=32, required=True)
    email = forms.CharField(label="Email", max_length=64, required=True)
    website = forms.CharField(label="Url", required=False)
    message = forms.CharField(label="Message", required=True, widget=forms.Textarea())