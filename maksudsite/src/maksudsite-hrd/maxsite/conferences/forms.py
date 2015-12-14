from django import forms
from django.template.loader import render_to_string
from maxsite.models import Conference, ConferenceCategory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

class ConferenceCategoryForm(forms.ModelForm):
    id = forms.CharField(label="id", widget=forms.HiddenInput(), required=False)
    # category = forms.ModelMultipleChoiceField(queryset=ConferenceCategory.objects.all())
    class Meta:
        model = ConferenceCategory

class ConferenceForm(forms.ModelForm):
    id = forms.CharField(label="id", widget=forms.HiddenInput(), required=False)
    # category = forms.ModelMultipleChoiceField(queryset=ConferenceCategory.objects.all())
    class Meta:
        model = Conference
        
class ConferenceImportForm(forms.Form):
    id = forms.CharField(label="id", widget=forms.HiddenInput(), required=False)
#     name = forms.CharField(label="Name", required=False)
    file = forms.FileField(label="File", widget=forms.FileInput(), required=False)
 
#     radio_buttons = forms.ChoiceField(
#         choices = (
#             ('option_one', "Option one is this and that be sure to include why it's great"), 
#             ('option_two', "Option two can is something else and selecting it will deselect option one")
#         ),
#         widget = forms.RadioSelect,
#         initial = 'option_two',
#     )
#  
#     checkboxes = forms.MultipleChoiceField(
#         choices = (
#             ('option_one', "Option one is this and that be sure to include why it's great"), 
#             ('option_two', 'Option two can also be checked and included in form results'),
#             ('option_three', 'Option three can yes, you guessed it also be checked and included in form results')
#         ),
#         initial = 'option_one',
#         widget = forms.CheckboxSelectMultiple,
#         help_text = "<strong>Note:</strong> Labels surround all the options for much larger click areas and a more usable form.",
#     )
#  
#     appended_text = forms.CharField(
#         help_text = "Here's more help text"
#     )
#  
#     prepended_text = forms.CharField()
#  
#     prepended_text_two = forms.CharField()
#  
#     multicolon_select = forms.MultipleChoiceField(
#         choices = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')),
#     )
 
    # Uni-form
#     helper = FormHelper()
#     helper.form_class = 'form-horizontal'
#     helper.layout = Layout(
#         Field('text_input', css_class='input-xlarge'),
#         Field('textarea', rows="3", css_class='input-xlarge'),
#         'radio_buttons',
#         Field('checkboxes', style="background: #FAFAFA; padding: 10px;"),
#         AppendedText('appended_text', '.00'),
#         PrependedText('prepended_text', '<input type="checkbox" checked="checked" value="" id="" name="">', active=True),
#         PrependedText('prepended_text_two', '@'),
#         'multicolon_select',
#         FormActions(
#             Submit('save_changes', 'Save changes', css_class="btn-primary"),
#             Submit('cancel', 'Cancel'),
#         )
#     )