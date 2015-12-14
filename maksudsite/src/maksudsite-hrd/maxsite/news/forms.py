from django import forms
from django.template.loader import render_to_string
from maxsite.models import News
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


class NewsForm(forms.ModelForm):
    id = forms.CharField(label="id", widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = News