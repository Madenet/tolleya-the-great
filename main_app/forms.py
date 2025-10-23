from django import forms
from django.forms.widgets import DateInput, TextInput
from django.forms import CheckboxSelectMultiple
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Row, Column
from college.models import CollegeAndUniversities
from bursary.models import Bursary
from .models import *

class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        # Here make some changes such as:
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

#custom user form
class CustomUserForm(FormSettings):
    email = forms.EmailField(required=True)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')])
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    address = forms.CharField(widget=forms.Textarea)
    password = forms.CharField(widget=forms.PasswordInput)
    widget = {
        'password': forms.PasswordInput(),
    }
    profile_pic = forms.ImageField()

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)

        if kwargs.get('instance'):
            instance = kwargs.get('instance').admin.__dict__
            self.fields['password'].required = False
            for field in CustomUserForm.Meta.fields:
                self.fields[field].initial = instance.get(field)
            if self.instance.pk is not None:
                self.fields['password'].widget.attrs['placeholder'] = "Fill this only if you wish to update password"

    def clean_email(self, *args, **kwargs):
        formEmail = self.cleaned_data['email'].lower()
        if self.instance.pk is None:  # Insert
            if CustomUser.objects.filter(email=formEmail).exists():
                raise forms.ValidationError(
                    "The given email is already registered")
        else:  # Update
            dbEmail = self.Meta.model.objects.get(
                id=self.instance.pk).admin.email.lower()
            if dbEmail != formEmail:  # There has been changes
                if CustomUser.objects.filter(email=formEmail).exists():
                    raise forms.ValidationError("The given email is already registered")

        return formEmail

    class Meta:
        model = CustomUser
        fields = ['first_name','last_name', 'email', 'gender',  'password','profile_pic', 'address' ]

#student Form
class StudentForm(CustomUserForm):
    class Meta(CustomUserForm.Meta):
        model = Student
        fields = CustomUserForm.Meta.fields + ['school', 'grade', 'course', 'session', 'circuit']

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)

        # Mark required fields
        required_fields = ['circuit', 'school', 'grade', 'course', 'session']
        for field in required_fields:
            if field in self.fields:
                self.fields[field].required = True

        # Optional: Add Bootstrap styling
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
  

#educator
class EducatorForm(CustomUserForm):
    class Meta(CustomUserForm.Meta):
        model = Educator
        fields = CustomUserForm.Meta.fields + [
            'circuit', 'school', 'grade', 'session', 'term', 'course', 'subjects'
        ]

    def __init__(self, *args, **kwargs):
        super(EducatorForm, self).__init__(*args, **kwargs)

        # Add missing model fields to form manually
        self.fields['circuit'] = forms.ModelChoiceField(
            queryset=Circuit.objects.all(),
            required=True,
            label="Circuit"
        )
        self.fields['school'] = forms.ModelChoiceField(
            queryset=School.objects.all(),
            required=True,
            label="School"
        )
        self.fields['grade'] = forms.ModelChoiceField(
            queryset=Grade.objects.all(),
            required=True,
            label="Grade"
        )
        self.fields['session'] = forms.ModelChoiceField(
            queryset=Session.objects.all(),
            required=True,
            label="Session"
        )
        self.fields['term'] = forms.ModelChoiceField(
            queryset=Term.objects.all(),
            required=True,
            label="Term"
        )
        self.fields['course'] = forms.ModelChoiceField(
            queryset=Course.objects.all(),
            required=True,
            label="Course"
        )
        self.fields['subjects'] = forms.ModelMultipleChoiceField(
            queryset=Subject.objects.all(),
            required=True,
            widget=forms.SelectMultiple(attrs={'size': 5}),
            label="Subjects"
        )

        # Add Bootstrap classes
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        # Crispy layout (optional)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('circuit', css_class='form-group col-md-6'),
                Column('school', css_class='form-group col-md-6'),
            ),
            Row(
                Column('grade', css_class='form-group col-md-4'),
                Column('session', css_class='form-group col-md-4'),
                Column('term', css_class='form-group col-md-4'),
            ),
            Row(
                Column('course', css_class='form-group col-md-6'),
                Column('subjects', css_class='form-group col-md-6'),
            )
        )

#member
class MemberForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)
        
        # Optional: Add Bootstrap styling
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta(CustomUserForm.Meta):
        model = Member
        fields = CustomUserForm.Meta.fields + ['school', 'position', 'session', 'term']

#cwa user
class CWA_AdminForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(CWA_AdminForm, self).__init__(*args, **kwargs)
        
        # Optional: Add Bootstrap styling
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta(CustomUserForm.Meta):
        model = CWA_Admin
        fields = CustomUserForm.Meta.fields + ['school', 'collegeanduniversity', 'bursary', 'session', 'term']

#parent form
class ParentForm(CustomUserForm):
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=True
    )
    school = forms.ModelChoiceField(
        queryset=School.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    session = forms.ModelChoiceField(
        queryset=Session.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    term = forms.ModelChoiceField(
        queryset=Term.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    relationship = forms.ChoiceField(
        choices=Parent.RELATIONSHIP_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    employment_status = forms.ChoiceField(
        choices=Parent.EMPLOYMENT_STATUS,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    occupation = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    education_level = forms.ChoiceField(
        choices=Parent.EDUCATION_LEVELS,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta(CustomUserForm.Meta):
        model = Parent
        fields = CustomUserForm.Meta.fields + [
            'school', 'students', 'session', 'term',
            'relationship', 'employment_status', 'occupation', 'education_level'
        ]
        
#principal form
class PrincipalForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(PrincipalForm, self).__init__(*args, **kwargs)
        
        # Make specific fields required
        self.fields['circuit'].required = True
        self.fields['school'].required = True
        self.fields['grade'].required = True

        # Optional: Add Bootstrap styling
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta(CustomUserForm.Meta):
        model = Principal
        fields = CustomUserForm.Meta.fields + ['circuit', 'school', 'grade', 'subject', 'term', 'course']


#principal edit form
class PrincipalEditForm(forms.ModelForm):
    class Meta:
        model = Principal
        fields = ['admin', 'circuit', 'school']
        widgets = {
            'admin': forms.HiddenInput(),  # Keep the admin field hidden
        }

    # Custom fields for the CustomUser associated with Principal
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    address = forms.CharField(widget=forms.Textarea, required=False)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], required=False)
    profile_pic = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super(PrincipalEditForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            self.fields['first_name'].initial = kwargs['instance'].admin.first_name
            self.fields['last_name'].initial = kwargs['instance'].admin.last_name
            self.fields['address'].initial = kwargs['instance'].admin.address
            self.fields['gender'].initial = kwargs['instance'].admin.gender
            self.fields['profile_pic'].initial = kwargs['instance'].admin.profile_pic

    def save(self, commit=True):
        principal = super(PrincipalEditForm, self).save(commit=False)
        admin = principal.admin
        
        # Update the CustomUser fields
        admin.first_name = self.cleaned_data['first_name']
        admin.last_name = self.cleaned_data['last_name']
        admin.address = self.cleaned_data['address']
        admin.gender = self.cleaned_data['gender']
        
        if 'profile_pic' in self.cleaned_data and self.cleaned_data['profile_pic']:
            admin.profile_pic = self.cleaned_data['profile_pic']
        
        if commit:
            admin.save()  # Save the CustomUser instance
            principal.save()  # Save the Principal instance

        return principal

#cwa_admin edit form
class CWA_AdminEditForm(forms.ModelForm):
    class Meta:
        model = CWA_Admin
        fields = ['admin', 'school', 'collegeanduniversity', 'bursary']
        widgets = {
            'admin': forms.HiddenInput(),  # Keep the admin field hidden
        }

    # Custom fields for the CustomUser associated with cwa-admin
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    address = forms.CharField(widget=forms.Textarea, required=False)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], required=False)
    position = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    profile_pic = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super(PrincipalEditForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            self.fields['first_name'].initial = kwargs['instance'].admin.first_name
            self.fields['last_name'].initial = kwargs['instance'].admin.last_name
            self.fields['address'].initial = kwargs['instance'].admin.address
            self.fields['gender'].initial = kwargs['instance'].admin.gender
            self.fields['profile_pic'].initial = kwargs['instance'].admin.profile_pic

    def save(self, commit=True):
        principal = super(PrincipalEditForm, self).save(commit=False)
        admin = principal.admin
        
        # Update the CustomUser fields
        admin.first_name = self.cleaned_data['first_name']
        admin.last_name = self.cleaned_data['last_name']
        admin.address = self.cleaned_data['address']
        admin.gender = self.cleaned_data['gender']
        
        if 'profile_pic' in self.cleaned_data and self.cleaned_data['profile_pic']:
            admin.profile_pic = self.cleaned_data['profile_pic']
        
        if commit:
            admin.save()  # Save the CustomUser instance
            principal.save()  # Save the Principal instance

        return principal
    
#circuit manager
class Circuit_ManagerForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(Circuit_ManagerForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Circuit_Manager
        fields = CustomUserForm.Meta.fields + \
            ['circuit']
    #attendancereport, subject, course, session, term, student, educator, parent, principal, member, studentresult, 


#termform
class TermForm(forms.ModelForm):
    class Meta:
        model = Term
        fields = ['term_name', 'is_current', 'session', 'next_term_begins']
        widgets = {
            'term_name': forms.Select(attrs={'class': 'form-control'}),
            'is_current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'session': forms.Select(attrs={'class': 'form-control'}),
            'next_term_begins': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

#admin
class AdminForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Admin
        fields = CustomUserForm.Meta.fields

#edit educator profile

#staff
class StaffForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Staff
        fields = CustomUserForm.Meta.fields + \
            ['course' ]


#courseform
class CourseForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)

    class Meta:
        fields = ['name','school']
        model = Course

#gradeform
class GradeForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(GradeForm, self).__init__(*args, **kwargs)

    class Meta:
        fields = ['name']
        model = Grade

#subject
class SubjectForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Subject
        fields = ['name', 'course', 'grade']


#session
class SessionForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(SessionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Session
        fields = '__all__'
        widgets = {
            'start_year': DateInput(attrs={'type': 'date'}),
            'end_year': DateInput(attrs={'type': 'date'}),
        }


#term
class TermForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(TermForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Term
        fields = ['term_name','is_current','activity_description','session','next_term_begins']
        widgets = {
            'start_year': DateInput(attrs={'type': 'date'}),
            'end_year': DateInput(attrs={'type': 'date'}),
            'term_name': forms.Select(attrs={'class': 'form-control'}),
            'is_current': forms.TextInput(attrs={'class': 'form-control'}),
            'activity_description': forms.TextInput(attrs={'class': 'form-control'}),
            'session': forms.Select(attrs={'class': 'form-control'}),
            'next_term_begins': DateInput(attrs={'type': 'date'}),
        }

#leavereport
class LeaveReportStaffForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportStaffForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportStaff
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }


#feedback staff
class FeedbackStaffForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackStaffForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackStaff
        fields = ['feedback']


#leavereport student
class LeaveReportStudentForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportStudentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportStudent
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }


#feedback
class FeedbackStudentForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackStudentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackStudent
        fields = ['feedback']


#student edit form
class StudentEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StudentEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Student
        fields = CustomUserForm.Meta.fields 


#staff edit form
class StaffEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StaffEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Staff
        fields = CustomUserForm.Meta.fields

#circuit manager edit form
class CircuitManagerEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StaffEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Circuit_Manager
        fields = CustomUserForm.Meta.fields


#Edit Result form
class EditResultForm(FormSettings):
    session_list = Session.objects.all()
    session_year = forms.ModelChoiceField(
        label="Session Year", queryset=session_list, required=True)

    def __init__(self, *args, **kwargs):
        super(EditResultForm, self).__init__(*args, **kwargs)

    class Meta:
        model = StudentResult
        fields = ['session_year', 'subject', 'student', 'test', 'assignment', 'exam']

#school form
class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = [
            'emis', 'name', 'contact', 'phase', 'sector', 'educators_on_db',
            'school_type', 'school_term', 'logo', 'head_principal', 'deputy',
            'filter_by', 'website_url', 'email', 'whatsapp_number', 'grade',
            'address', 'year', 'count'
        ]
        widgets = {
            'emis': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.Select(attrs={'class': 'form-control'}),  # Select for choices
            'phase': forms.TextInput(attrs={'class': 'form-control'}),
            'sector': forms.TextInput(attrs={'class': 'form-control'}),
            'educators_on_db': forms.NumberInput(attrs={'class': 'form-control'}),
            'school_type': forms.Select(attrs={'class': 'form-control'}),  # Select for choices
            'school_term': forms.TextInput(attrs={'class': 'form-control'}), # Select for choices
            'filter_by': forms.Select(attrs={'class': 'form-control'}),  # Select for choices
            'website_url': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),  # Email field
            'whatsapp_number': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'count': forms.NumberInput(attrs={'class': 'form-control'}),
        }


        
#school dashboard phase
class SchoolEditForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name', 'logo', 'head_principal', 'deputy', 'school_type', 'filter_by', 'website_url', 'email', 'grade', 'whatsapp_number', 'address', 'year']


# documents upload
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['name', 'email', 'phone', 'department', 'message']
        fields = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rowas': 4}),
        }

# subscription
class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'forms-control',
                'placeholder': 'Enter your email'
            }),
        }

#timetable form
class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = ['day', 'grade', 'course', 'subjects', 'educators', 'start_time', 'end_time']
        widgets = {
            'subjects': forms.SelectMultiple(attrs={'size': 5}),
            'educators': forms.SelectMultiple(attrs={'size': 5}),
        }

#messages
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text', 'reply_to']  # 'text' for the message, media will be handled separately
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type a message...'}),
            'reply_to': forms.HiddenInput(),
        }

    media_files = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}),
        required=False
    )

#school perfomance

class SchoolPerformanceForm(forms.ModelForm):
    class Meta:
        model = SchoolPerformance
        fields = [
            'school_record', 'session', 'educator', 'subject', 'grade', 
            'school_principal', 'performance_score', 'comments'
        ]

#reply contact
class ReplyContactForm(forms.Form):
    subject = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

class ProspectorForm(forms.ModelForm):
    class Meta:
        model = Prospectors
        fields = ['institution', 'address', 'copy', 'logo']

#custom password reset
class CustomPasswordResetForm(forms.Form):
    email = forms.EmailField(
        label="Enter your email",
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("No user with this email address found.")
        return email


class NewsAndEventsForm(forms.ModelForm):
    class Meta:
        model = NewsAndEvents
        fields = ['title', 'summary', 'posted_as', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'summary': forms.Textarea(attrs={'class': 'form-control'}),
            'posted_as': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }