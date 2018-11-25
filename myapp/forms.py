from django import forms
from django.core import validators

# def check_alt_lim(value):
#     if value>90 or value<0:
#         raise forms.ValidationError("Please enter a value between 0 and 90.")
#
# def check_edw_lim(value):
#     if value>120000 or value<0:
#         raise forms.ValidationError("Please enter a value between 0 and 120000.")

class FormName(forms.Form):
	edw = forms.FloatField(help_text='Enter a value between 0 and 120,000.',initial=45000,label='Edw  [Effective daylight on window]')
	alt = forms.FloatField(help_text='Enter a value between 0 and 90.',initial=45,label='Alt  [Solar Elevation Angle]')
