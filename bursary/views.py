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
from .models import Bursary
from django.template.loader import render_to_string, get_template 
from django.urls import reverse_lazy
from .forms import BursaryForm
from django.core.mail import send_mass_mail
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail, EmailMessage


#Bursary Functions

def bursary_list_view(request):
    """Show list of all bursaries"""
    bursaries = Bursary.objects.all().order_by("-upload_time")
    return render(request, "bursary/bursary_list.html", {"bursaries": bursaries})

# Use the active user model (CustomUser)
User = get_user_model()

#bursaries added
def bursary_add_view(request):
    """Add a new bursary"""
    if request.method == "POST":
        form = BursaryForm(request.POST, request.FILES)
        if form.is_valid():
            bursary = form.save()

            # Email content
            subject = f"New Bursary Available: {bursary.title}"
            listview_url = "https://www.elimcircuit.com/bursarybursaries/"
            raw_message = (
                f"A new bursary titled '{bursary.title}' has just been added to the platform. "
                f"<br><br>Apply now 👉 <a href='{listview_url}'>{listview_url}</a>"
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
                "name": "Elim Circuit Community",
                "message": raw_message
            }
            email_template = get_template("emailapp/email.html").render(context)

            email = EmailMessage(
                subject=subject,
                body=email_template,
                from_email=from_email,
                to=[],  # no "to" field
                bcc=recipient_list  # hidden bulk email
            )
            email.content_subtype = "html"
            email.send(fail_silently=False)

            messages.success(request, "Bursary added successfully and email notifications sent.")
            return redirect("bursary_list")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = BursaryForm()

    return render(request, "bursary/bursary_add.html", {"form": form})


def bursary_update_view(request, pk):
    """Update an existing bursary"""
    bursary = get_object_or_404(Bursary, pk=pk)
    if request.method == "POST":
        form = BursaryForm(request.POST, request.FILES, instance=bursary)
        if form.is_valid():
            form.save()
            messages.success(request, "Bursary updated successfully.")
            return redirect("bursary_list")
    else:
        form = BursaryForm(instance=bursary)
    return render(request, "bursary/bursary_add.html", {"form": form})


def bursary_delete_view(request, pk):
    """Delete a bursary"""
    bursary = get_object_or_404(Bursary, pk=pk)
    bursary.delete()
    messages.success(request, "Bursary successfully deleted.")
    return redirect("bursary_list")


def bursary_detail(request, pk):
    bursary = get_object_or_404(Bursary, pk=pk)
    return render(request, 'bursary/bursary_detail.html', {'bursary': bursary})