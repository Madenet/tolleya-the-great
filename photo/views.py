from django.shortcuts import render, redirect
from .models import Photo
from job.models import Category
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string, get_template
from django.urls import reverse_lazy, reverse 
# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
import os


#gallery
def gallery(request):
    user = request.user
    category = request.GET.get('category')
    if category == None:
        photos = Photo.objects.filter(category__user=user)
    else:
        photos = Photo.objects.filter(
            category__name=category, category__user=user)

    categories = Category.objects.filter(user=user)
    context = {'categories': categories, 'photos': photos}
    return render(request, 'photos/gallery.html', context)

#view phot propfirms
def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    return render(request, 'photos/photo.html', {'photo': photo})

#approve photo
def approve_photos(request):
    if not request.user.is_staff:  # Restrict access to staff members
        messages.error(request, "You don't have permission to approve photos.")
        return redirect('listview')  # Redirect to gallery if unauthorized

    photos = Photo.objects.filter(approval_status='pending')

    if request.method == 'POST':
        photo_id = request.POST.get('photo_id')
        action = request.POST.get('action')

        if photo_id and action:
            photo = Photo.objects.get(id=photo_id)
            if action == "approve":
                photo.approval_status = "approved"
                messages.success(request, "Photo approved successfully.")
            elif action == "reject":
                photo.delete()
                messages.success(request, "Photo rejected and deleted.")
            photo.save()
        
        return redirect('approve_photos')

    return render(request, 'photos/approve_photos.html', {'photos': photos})

#add photo
def addPhoto(request):
    user = request.user
    categories = user.category_set.all()

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(
                user=user,
                name=data['category_new'])
        else:
            category = None
        
        if image:
            photo = Photo.objects.create(
                author=user,
                category=category,
                description=data['description'],
                image=image,
                approval_status='pending',  # Set photo status to pending
                website_url=data.get('website_url', ''),
                gmail_url=data.get('gmail_url', ''),
                whatsapp_number=data.get('whatsapp_number', ''),
                facebook_url=data.get('facebook_url', ''),
                tiktok_url=data.get('tiktok_url', ''),
                location=data.get('location', ''),
                twitter_url=data.get('twitter_url', ''),
                playstore_url=data.get('playstore_url', ''),
                linkedin_url=data.get('linkedin_url', ''),
                instagram_url=data.get('instagram_url', ''),
                pinterest_url=data.get('pinterest_url', ''),
                youtube_url=data.get('youtube_url', ''),
            )

          
            return redirect('listview')  # Make sure the URL name is correct
        else:
            error_message = "Please upload the main image."
            context = {'categories': categories, 'error_message': error_message}
            return render(request, 'photos/add.html', context)

    context = {'categories': categories}
    return render(request, 'photos/add.html', context)


#galleryview
def galleryview(request):
    photos = Photo.objects.filter(approval_status='approved')  # Only show approved photos
    context = {'photos': photos}
    template = 'photos/listview.html'    
    return render(request, template, context)

#delete gallery image
def deletePhoto(request, pk):
    photos = Photo.objects.get(id=pk)
    if len(photos.image) > 0:
        os.remove(photos.image.path)
    photos.delete()
    messages.success(request,"Product Deleted Successfuly")
    return redirect('listview')

#category view
# Category view - Fetching photos based on category
def CategoryView(request, category):
    user = request.user
    category_instance = Category.objects.filter(name=category, user=user).first()

    if category_instance:
        category_photos = Photo.objects.filter(category=category_instance)
    else:
        category_photos = Photo.objects.none()  # Return an empty queryset if no category is found

    return render(request, 'social/categories.html', {'category_photos': category_photos})


#edit the phot
def edit_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    
    if request.method == "POST":
        photo.category_id = request.POST.get("category") or None
        photo.image = request.FILES.get("image", photo.image)
        photo.video = request.FILES.get("video", photo.video)
        photo.website_url = request.POST.get("website_url", "")
        photo.gmail_url = request.POST.get("gmail_url", "")
        photo.whatsapp_number = request.POST.get("whatsapp_number", "")
        photo.facebook_url = request.POST.get("facebook_url", "")
        photo.tiktok_url = request.POST.get("tiktok_url", "")
        photo.zoom_url = request.POST.get("zoom_url", "")
        photo.microsoftTeam_url = request.POST.get("microsoftTeam_url", "")
        photo.location = request.POST.get("location", "")
        photo.twitter_url = request.POST.get("twitter_url", "")
        photo.playstore_url = request.POST.get("playstore_url", "")
        photo.linkedin_url = request.POST.get("linkedin_url", "")
        photo.instagram_url = request.POST.get("instagram_url", "")
        photo.pinterest_url = request.POST.get("pinterest_url", "")
        photo.youtube_url = request.POST.get("youtube_url", "")
        photo.description = request.POST.get("description", "")

        photo.save()  # Save the updated data
        return redirect('gallery')  # Redirect to gallery after editing

    return render(request, 'photos/edit_photo.html', {'photo': photo})