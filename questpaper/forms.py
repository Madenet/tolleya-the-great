# forms.py
from django import forms
from .models import QuestionPaper, Department, Topic
from main_app.models import School, Educator, Grade

class QuestionPaperUploadForm(forms.ModelForm):
    class Meta:
        model = QuestionPaper
        fields = [
            'school', 'grade', 'term', 'department', 'complexity_rating', 
            'topics', 'number_of_questions', 'file'
        ]
        widgets = {
            'school': forms.Select(attrs={'class': 'form-control'}),
            'grade': forms.Select(attrs={'class': 'form-control'}),
            'term': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'complexity_rating': forms.Select(attrs={'class': 'form-control'}),
            'topics': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-inline'}),  # Added class for inline checkboxes
            'number_of_questions': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
