from django import forms
from .models import *

class CustomForm(forms.Form):
    status = forms.CharField()
    message = forms.CharField()
    subject = forms.CharField()
    
#option form
class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ('Full_Names', 'address', 'body', 'Where_to_Apply', 'header_image', 'image', 'application_from', 'price')
        widgets = {
            'Full_Names': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.HiddenInput(),  # Hide the author field
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'Where_to_Apply': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'oninput': 'calculateTotal()'}),  # Add an oninput event to calculate the total price
        }

        labels = {
            'price': 'Price (R)',  # Change label for price field
        }
        