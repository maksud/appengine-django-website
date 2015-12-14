from django import forms
from maxsite.models import AppDocument

#class DocumentUploadForm2(forms.Form):
#    id = forms.CharField(label="id", widget=forms.HiddenInput(), required=False)
#    name = forms.CharField(label="Name", max_length=120, required=True, widget=forms.TextInput())
#    title = forms.CharField(label="Title", max_length=255, required=True, widget=forms.TextInput())
#    file = forms.FileField(label="File", widget=forms.FileInput(), required=False)


class DocumentUploadForm(forms.ModelForm):
    id = forms.CharField(label="id", widget=forms.HiddenInput(), required=False)
    name = forms.CharField(label="Name", required=False)
    document = forms.FileField(label="File", widget=forms.FileInput(), required=False)
    class Meta:
        model = AppDocument
        exclude = ('file_name','content_type','content_length','blob_key')
        
        
        

