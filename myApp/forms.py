# forms.py
from django import forms
from myApp.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit




class Payment_Get_Way_Form(forms.ModelForm):
    class Meta:
        model=Payment_Get_Way
        fields='__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout('name', 'amount')
        self.helper.add_input(Submit('submit', 'Submit'))


