from django.shortcuts import render
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.views.generic import CreateView, ListView
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import PasswordChangeForm
from django_filters.views import FilterView
from django.views.generic import ListView, CreateView, DeleteView
from .models import CollegeAndUniversities
from django.urls import reverse_lazy
from .forms import CollegeAndUniversitiesForm
from django.core.mail import send_mass_mail
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string, get_template 



def college_list_view(request):
    colleges = CollegeAndUniversities.objects.all().order_by("-upload_time")
    return render(request, "college/college_list.html", {"colleges": colleges})

# Use the active user model (CustomUser)
User = get_user_model()


def college_add_view(request):
    if request.method == "POST":
        form = CollegeAndUniversitiesForm(request.POST, request.FILES)
        if form.is_valid():
            college = form.save()

            # Email content
            subject = f"New University Added: {college.title}"
            listview_url = "https://www.elimcircuit.com/collegecolleges/"
            raw_message = (
                f"A new university '{college.title}' has just been added to the platform. "
                f"<br><br>Check it out here 👉 <a href='{listview_url}'>{listview_url}</a>"
            )

            from_email = settings.DEFAULT_FROM_EMAIL

            # Get all valid email addresses
            recipient_list = list(
                User.objects.exclude(email__isnull=True)
                            .exclude(email__exact="")
                            .values_list('email', flat=True)
            )

            # Prepare HTML email
            context = {
                "name": "Elim Circuit Community",  # generic name for all
                "message": raw_message
            }
            email_template = get_template("emailapp/email.html").render(context)

            email = EmailMessage(
                subject=subject,
                body=email_template,
                from_email=from_email,
                to=[],  # leave this empty
                bcc=recipient_list  # this sends to all, hidden from each other like BCC in Gmail
            )
            email.content_subtype = "html"
            email.send(fail_silently=False)

            messages.success(request, "College/University added and email sent to all users.")
            return redirect("college_list")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = CollegeAndUniversitiesForm()

    return render(request, "college/college_form.html", {"form": form})



def college_update_view(request, pk):
    college = get_object_or_404(CollegeAndUniversities, pk=pk)
    if request.method == "POST":
        form = CollegeAndUniversitiesForm(request.POST, request.FILES, instance=college)
        if form.is_valid():
            form.save()
            messages.success(request, "College/University updated successfully.")
            return redirect("college_list")
    else:
        form = CollegeAndUniversitiesForm(instance=college)
    return render(request, "college/college_form.html", {"form": form})


def college_delete_view(request, pk):
    college = get_object_or_404(CollegeAndUniversities, pk=pk)
    college.delete()
    messages.success(request, "college/University deleted successfully.")
    return redirect("college_list")

def college_detail(request, pk):
    college = get_object_or_404(CollegeAndUniversities, pk=pk)
    return render(request, 'college/college_detail.html', {'college': college})
