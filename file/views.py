import json
import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .EmailBackend import EmailBackend
from college.models import CollegeAndUniversities
from bursary.models import Bursary
from college.forms import CollegeAndUniversitiesForm
from django.views import generic
from django.views import View
from bursary.forms import BursaryForm
from django.core.mail import send_mail
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from main_app.models import *
from main_app.forms import *
from .models import *
from .forms import *
from django.utils.decorators import method_decorator
from django.core.mail import EmailMessage


# ########################################################
# File Upload views
# ########################################################

def handle_file_upload(request, slug):
    school = School.objects.get(slug=slug)
    if request.method == "POST":
        form = UploadFormFile(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.school = school
            obj.save()

            messages.success(
                request, (request.POST.get("title") + " has been uploaded.")
            )
            return redirect("school_detail", slug=slug)
    else:
        form = UploadFormFile()
    return render(
        request,
        "upload/upload_file_form.html",
        {"title": "File Upload", "form": form, "school": school},
    )




def handle_file_edit(request, slug, file_id):
    school = School.objects.get(slug=slug)
    instance = Upload.objects.get(pk=file_id)
    if request.method == "POST":
        form = UploadFormFile(request.POST, request.FILES, instance=instance)
        # file_name = request.POST.get('name')
        if form.is_valid():
            form.save()
            messages.success(
                request, (request.POST.get("title") + " has been updated.")
            )
            return redirect("school_detail", slug=slug)
    else:
        form = UploadFormFile(instance=instance)

    return render(
        request,
        "upload/upload_file_form.html",
        {"title": instance.title, "form": form, "school": school},
    )


def handle_file_delete(request, slug, file_id):
    file = Upload.objects.get(pk=file_id)
    # file_name = file.name
    file.delete()

    messages.success(request, (file.title + " has been deleted."))
    return redirect("school_detail", slug=slug)


#school details
def school_single(request, slug):
    school = School.objects.get(slug=slug)
    files = Upload.objects.filter(school__slug=slug)
    # videos = UploadVideo.objects.filter(school__slug=slug)

    # educators = User.objects.filter(allocated_educator__pk=school.id)
    educators = Educator.objects.filter(schools__pk=school.id)

    return render(
        request,
        "school/school_single.html",
        {
            "title": school.title,
            "school": school,
            "files": files,
            # "videos": videos,
            "educators": educators,
            "media_url": settings.MEDIA_ROOT,
        },
    )
