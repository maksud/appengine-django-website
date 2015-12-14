from django import forms
from maxsite.models import AppTemplate

class ContentsForm(forms.Form):
    id = forms.CharField(label="id", widget=forms.HiddenInput(), required=False)
    name = forms.CharField(label="Name", required=True)
    caption = forms.CharField(label="Caption", required=False)
    language = forms.CharField(label="Language", required=False)
    url = forms.CharField(label="Url", required=False)
    content = forms.CharField(label="Contents", required=True, widget=forms.Textarea())
    css = forms.CharField(label="CSS", required=False, widget=forms.Textarea())
    js = forms.CharField(label="JavaScript", required=False, widget=forms.Textarea())

class FontsForm(forms.Form):
    font_family = forms.CharField (label="Font Family", max_length=250, required=True)
    web_rating = forms.CharField (label="Rating", max_length=2, required=True)
    font_comments = forms.CharField (label="Comments", max_length=250, required=True)
    font_typeface = forms.CharField (label="Typeface", max_length=250, required=True)
    
class TemplateForm(forms.ModelForm):
    id = forms.CharField(label="id", widget=forms.HiddenInput(), required=False)
    class Meta:
        model = AppTemplate
