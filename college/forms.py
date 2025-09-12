from django import forms
from .models import CollegeAndUniversities

class CollegeAndUniversitiesForm(forms.ModelForm):
    class Meta:
        model = CollegeAndUniversities
        fields = ['title', 'summary', 'website_url', 'picture', 'posted_as']
