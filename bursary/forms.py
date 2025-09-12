# In forms.py
from django import forms
from .models import Bursary

class BursaryForm(forms.ModelForm):
    class Meta:
        model = Bursary
        fields = ['title', 'summary', 'website_url', 'picture', 'posted_as']

    def clean_picture(self):
        picture = self.cleaned_data.get('picture')
        if picture:
            if picture.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError("Image file too large ( > 5MB )")
            return picture
