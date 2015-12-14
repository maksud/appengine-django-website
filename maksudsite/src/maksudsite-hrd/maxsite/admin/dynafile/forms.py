from django import forms

class DynaUploadForm(forms.Form):
    file = forms.FileField(label="File", widget=forms.FileInput(), required=True)
    
class DynaTextForm(forms.Form):
    id = forms.CharField(label="id", widget=forms.HiddenInput(), required=False)
    name = forms.CharField(label="Filename", required=True)
    content_type = forms.CharField(label="Content Type", required=True)
    content = forms.CharField(label="Content", required=True, widget=forms.Textarea())    