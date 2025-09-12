from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.models import User 
from django.template.loader import render_to_string, get_template 
from django.urls import reverse_lazy, reverse
from .models import Application, University
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.views.generic import ListView, CreateView
from django.contrib import messages
from django.contrib.auth import get_user_model

import os

#gallery

def gallery(request):
    user = request.user
    university = request.GET.get('university')
    if university == None:
        applications = Application.objects.university(university__user=user)
    else:
        applications = Application.objects.university(
            university__name=university, university__user=user)

    universitys = University.objects.university(user=user)
    context = {'universitys': universitys, 'applications': applications}
    return render(request, 'applications/applicationgallery.html', context)



#view phot propfirms
def viewApplication(request, pk):
    application = Application.objects.get(id=pk)
    return render(request, 'applications/application.html', {'application': application})


# add application
def addApplication(request):
    user = request.user
    universitys = user.university_set.all()

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')  # Try to get the main image

        # Handle university selection
        if data['university'] != 'none':
            university = University.objects.get(id=data['university'])
        elif data['university_new'] != '':
            university, _ = University.objects.get_or_create(user=user, name=data['university_new'])
        else:
            university = None

        # Try to create application with image
        try:
            application = Application.objects.create(
                author=user,
                university=university,
                keen=data.get('keen', ''),
                image=image,
                student=data.get('student', ''),
                address=data.get('address', ''),
                disability=data.get('disability', ''),
                varsity=data.get('varsity', ''),
                bursary=data.get('bursary', ''),
                details=data.get('details', ''),
            )
        except (ClientError, ValidationError, Exception) as e:
            logger.error(f"Image upload failed: {e}")
            application = Application.objects.create(
                author=user,
                university=university,
                keen=data.get('keen', ''),
                student=data.get('student', ''),
                address=data.get('address', ''),
                disability=data.get('disability', ''),
                varsity=data.get('varsity', ''),
                bursary=data.get('bursary', ''),
                details=data.get('details', ''),
            )

        # Show success message to user
        messages.success(request, "Your application was submitted successfully. You can now upload your documents.")

        return redirect('uploadfile')

    context = {'universitys': universitys}
    return render(request, 'applications/addapplication.html', context)


#galleryview
def galleryview(request):
	applications = Application.objects.all()
	context = {'applications': applications}
	template = 'applications/listview.html'	
	return render(request, template, context)

#delete gallery image
def deleteApplication(request, pk):
    applications = Application.objects.get(id=pk)
    if len(applications.image) > 0:
        os.remove(applications.image.path)
    applications.delete()
    messages.success(request,"Product Deleted Successfuly")
    return redirect('listview')

#university view
def UniversityView(request, university):
    user = request.user
    university_applications = Application.objects.university(user=user)
    return render(request, 'applications/universitys.html', { university_applications : university_applications})

#add university
def AddUniversityView(request):
    if request.method == 'POST':
        # Handle form submission to add the university to the database
        # This could involve creating a new instance of the University model
        # For simplicity, let's assume the form contains fields for university name, location, etc.
        name = request.POST.get('name')
        # Create a new University instance
        university = University.objects.create(name=name)
        # You can add more fields as needed
        return render(request, 'home.html')  # Render a success page
    else:
        return render(request, 'applications/adduniversity.html')  # Render the form for adding a university