from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .forms import * # Make sure to create this form
from .models import *  # Import the necessary models

def member_home(request):
    member = get_object_or_404(Member, admin=request.user)
    items = NewsAndEvents.objects.all().order_by("-updated_date")

    context = {
        "title": "News & Events",
        "items": items,
        'page_title': 'Member Dashboard',
    }
    return render(request, 'member_template/home_content.html', context)

def member_view_attendance(request):
    member = get_object_or_404(Member, admin=request.user)
    attendance_reports = AttendanceReport.objects.filter(member=member)
    items = NewsAndEvents.objects.all().order_by("-updated_date")

    context = {
        "title": "News & Events",
        "items": items,
        'page_title': 'View Attendance',
        'attendance_reports': attendance_reports,
    }
    return render(request, 'member_template/view_attendance.html', context)

def member_view_profile(request):
    member = get_object_or_404(Member, admin=request.user)
    form = MemberForm(request.POST or None, instance=member)

    context = {
        'form': form,
        'page_title': 'View/Update Profile'
    }

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect(reverse('member_view_profile'))
        else:
            messages.error(request, "Error updating profile!")

    return render(request, 'member_template/view_profile.html', context)

def member_manage_attendance_reports(request):
    member = get_object_or_404(Member, admin=request.user)
    attendance_reports = AttendanceReport.objects.filter(member=member)

    context = {
        'page_title': 'Manage Attendance Reports',
        'attendance_reports': attendance_reports,
    }
    return render(request, 'member_template/manage_attendance_reports.html', context)

def member_add_attendance_report(request):
    member = get_object_or_404(Member, admin=request.user)

    if request.method == 'POST':
        # Get data from POST request and create new AttendanceReport instance
        status = request.POST.get('status')
        attendance_report = AttendanceReport.objects.create(
            member=member,
            status=status
        )
        messages.success(request, "Attendance report added successfully!")
        return redirect(reverse('member_manage_attendance_reports'))
    else:
        messages.error(request, "Error adding attendance report. Please check the form.")

    context = {
        'page_title': 'Add Attendance Report'
    }
    return render(request, 'member_template/add_attendance_report.html', context)

def member_edit_attendance_report(request, report_id):
    report = get_object_or_404(AttendanceReport, id=report_id)

    if request.method == 'POST':
        # Update fields based on POST data
        report.status = request.POST.get('status')
        report.save()
        messages.success(request, "Attendance report updated successfully!")
        return redirect(reverse('member_manage_attendance_reports'))
    else:
        messages.error(request, "Error updating attendance report. Please check the form.")

    context = {
        'report': report,
        'page_title': 'Edit Attendance Report'
    }
    return render(request, 'member_template/edit_attendance_report.html', context)

def member_delete_attendance_report(request, report_id):
    report = get_object_or_404(AttendanceReport, id=report_id)
    if request.method == 'POST':
        report.delete()
        messages.success(request, "Attendance report deleted successfully!")
        return redirect(reverse('member_manage_attendance_reports'))

    context = {
        'report': report,
        'page_title': 'Delete Attendance Report'
    }
    return render(request, 'member_template/delete_attendance_report.html', context)

#advertisement view functions

#add ads
@csrf_exempt
def add_ad(request):
    if request.method == 'POST':
        # Get the data from the POST request
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        logo = request.FILES.get('logo')
        video = request.FILES.get('video')
        web_url = request.POST.get('web_url')
        whatsapp_number = request.POST.get('whatsapp_number')
        facebook_url = request.POST.get('facebook_url')
        tiktok_url = request.POST.get('tiktok_url')
        location = request.POST.get('location')
        playstore_url = request.POST.get('playstore_url')
        twitter_url = request.POST.get('twitter_url')
        linkedin_url = request.POST.get('linkedin_url')
        instagram_url = request.POST.get('instagram_url')
        pinterest_url = request.POST.get('pinterest_url')
        youtube_url = request.POST.get('youtube_url')
        share_id = request.POST.get('share_id')
        # Check if required fields are provided
        if not logo or not web_url:
            # If fields are missing, render the form with an error message
            return render(request, 'ads/add_ad.html', {'error': 'Please provide both logo and web URL.'})

        # Validate video size and duration if provided
        if video:
            validation_error = validate_video_size_and_duration(video)
            if validation_error:
                return render(request, 'ads/add_ad.html', {'error': validation_error})

        # Create a CustomAd instance with the provided data
        ad = CustomAd(
            title=title,
            description=description,
            logo=logo,
            video=video if video else None,
            web_url=web_url,
            whatsapp_number=whatsapp_number,
            facebook_url=facebook_url,
            location=location,
            twitter_url=twitter_url,
            playstore_url=playstore_url,
            linkedin_url=linkedin_url,
            instagram_url=instagram_url,
            tiktok_url=tiktok_url,
            pinterest_url=pinterest_url,
            youtube_url=youtube_url,
            share_id=share_id,
            user=request.user
        )

        try:
            # Save the ad to the database
            ad.save()
            # Redirect to the view_ads page after successful save
            return redirect('view_ads')
        except Exception as e:
            return render(request, 'ads/add_ad.html', {'error': f'An error occurred: {str(e)}'})

    # Handle non-POST requests or render the initial template if needed
    return render(request, 'ads/add_ad.html')



def view_ads(request):
    ads = CustomAd.objects.filter(user=request.user)
    return render(request, 'ads/view_ads.html', {'ads': ads})


def remove_ad(request, ad_id):
    ad = CustomAd.objects.get(pk=ad_id)
    if request.user == ad.user:
        ad.delete()
    return redirect('view_ads')

#share ad
def shared_ad(request, share_id):
    ad = get_object_or_404(CustomAd, share_id=share_id)
    return render(request, 'ads/shared_ad.html', {'ad': ad})

#terms of use and privacy policy
def terms_of_use(request):
    terms = TermsOfUse.objects.latest('last_updated')
    return render(request, 'terms_of_use.html', {'terms': terms})

def privacy_policy(request):
    privacy_policy = PrivacyPolicy.objects.latest('last_updated')
    return render(request, 'privacy_policy.html', {'privacy_policy': privacy_policy})

#payment and card method
#add ads

def add_payment(request):
    if request.method == 'POST':
        # Get the data from the request
        logo = request.FILES.get('logo')
        web_url = request.POST.get('web_url')
        
        # Check if required fields are provided
        if not logo or not web_url:
            return HttpResponse('Please provide both logo and web URL.', status=400)
        
        # Create a CustomAd instance
        ad = CustomAd(
            logo=logo,
            web_url=web_url,
            user=request.user
        )

        try:
            ad.save()
            return redirect('home')
        except Exception as e:
            return HttpResponse(f'An error occurred: {str(e)}', status=500)

    # Handle GET request (initial form display)
    return render(request, 'ads/add_payment.html')



def view_payments(request):
    ads = CustomAd.objects.filter(user=request.user)
    return render(request, 'ads/view_payments.html', {'ads': ads})


def remove_payment(request, ad_id):
    ad = CustomAd.objects.get(pk=ad_id)
    if request.user == ad.user:
        ad.delete()
    return redirect('view_payment')

#share ad
def shared_payment(request, share_id):
    ad = get_object_or_404(CustomAd, share_id=share_id)
    return render(request, 'ads/shared_payment.html', {'ad': ad})

#add card

def add_card(request):
    if request.method == 'POST':
        # Get the data from the request
        logo = request.FILES.get('logo')
        web_url = request.POST.get('web_url')
        
        # Check if required fields are provided
        if not logo or not web_url:
            return HttpResponse('Please provide both logo and web URL.', status=400)
        
        # Create a CustomAd instance
        ad = CustomAd(
            logo=logo,
            web_url=web_url,
            user=request.user
        )

        try:
            ad.save()
            return redirect('home')
        except Exception as e:
            return HttpResponse(f'An error occurred: {str(e)}', status=500)

    # Handle GET request (initial form display)
    return render(request, 'ads/add_card.html')



def view_cards(request):
    ads = CustomAd.objects.filter(user=request.user)
    return render(request, 'ads/view_cards.html', {'ads': ads})


def remove_card(request, ad_id):
    ad = CustomAd.objects.get(pk=ad_id)
    if request.user == ad.user:
        ad.delete()
    return redirect('view_card')

#share ad
def shared_card(request, share_id):
    ad = get_object_or_404(CustomAd, share_id=share_id)
    return render(request, 'ads/shared_card.html', {'ad': ad})