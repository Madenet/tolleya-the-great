from django.shortcuts import get_object_or_404, render, redirect
from .models import Job, Category, ApplyJob
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.contrib import messages
import os


#gallery

def jobgallery(request):
    user = request.user
    category = request.GET.get('category')
    if category == None:
        jobs = Job.objects.filter(category__user=user)
    else:
        jobs = Job.objects.filter(
            category__name=category, category__user=user)

    categories = Category.objects.filter(user=user)
    context = {'categories': categories, 'jobs': jobs}
    return render(request, 'jobs/jobgallery.html', context)

#view job

def viewJob(request, pk):
    job = Job.objects.get(id=pk)
    return render(request, 'jobs/job.html', {'job': job})

#add job
def addJob(request):
    user = request.user
    categories = user.category_set.all()

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')  # Get the main image

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(
                user=user,
                name=data['category_new'])
        else:
            category = None
       
        # Check if the main image is provided before creating the job instance
        if image:
            job = Job.objects.create(
                author=user,  # Set the author to the logged-in user
                category=category,
                description=data['description'],
                image=image,  # Use the main image
                website_url=data.get('website_url', ''),
                whatsapp_number=data.get('whatsapp_number', ''),
                facebook_url=data.get('facebook_url', ''),
                location=data.get('location', ''),
                twitter_url=data.get('twitter_url', ''),
                playstore_url=data.get('playstore_url', ''),
                linkedin_url=data.get('linkedin_url', ''),
                instagram_url=data.get('instagram_url', ''),
                pinterest_url=data.get('pinterest_url', ''),
                youtube_url=data.get('youtube_url', ''),
            )
            
            return redirect('joblistview')  # Make sure the URL name is correct
        else:
            error_message = "Please upload the main image."
            context = {'categories': categories, 'error_message': error_message}
            return render(request, 'jobs/add.html', context)

    context = {'categories': categories}
    return render(request, 'jobs/add.html', context)

#applyjob
def applyJob(request, job_id):
    user = request.user
    job = get_object_or_404(Job, id=job_id)
    categories = user.category_set.all()

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')
        cv = request.FILES.get('cv')

        # Determine category: use the job's category by default
        if data.get('category') and data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data.get('category_new'):
            category, created = Category.objects.get_or_create(
                user=user,
                name=data['category_new']
            )
        else:
            category = job.category  # fallback to the job's category

        if image and cv:
            ApplyJob.objects.create(
                category=category,
                full_names=data.get('full_names', ''),
                age=data.get('age', ''),
                address=data.get('address', ''),
                qualifications=data.get('qualifications', ''),
                motivation=data.get('motivation', ''),
                recent_jobs=data.get('recent_jobs', ''),
                position=data.get('position', ''),
                marital_status=data.get('marital_status', ''),
                experience=data.get('experience', ''),
                contacts=data.get('contacts', ''),
                whatsapp_no=data.get('whatsapp_no', ''),
                image=image,
                cv=cv,
            )
            messages.success(request, f"You have successfully applied for '{job.description}'!")
            return redirect('index')

        else:
            error_message = "Please upload both an image and your CV."
            context = {'categories': categories, 'job': job, 'error_message': error_message}
            return render(request, 'jobs/apply.html', context)

    context = {'categories': categories, 'job': job}
    return render(request, 'jobs/apply.html', context)

#applicationview
def applicationview(request):
	applyjobs = ApplyJob.objects.all()
	context = {'applyjobs': applyjobs}
	template = 'jobs/applicationview.html'	
	return render(request, template, context)

#delete application image
def deleteApplicationJob(request, pk):
    applyjobs = ApplyJob.objects.get(id=pk)
    if len(applyjobs.image) > 0:
        os.remove(applyjobs.image.path)
    applyjobs.delete()
    messages.success(request,"Product Deleted Successfuly")
    return redirect('joblistview')

#gallery
def jobgallery(request):
    user = request.user
    category = request.GET.get('category')
    if category == None:
        applyjobs = ApplyJob.objects.filter(category__user=user)
    else:
        applyjobs = ApplyJob.objects.filter(
            category__name=category, category__user=user)

    categories = Category.objects.filter(user=user)
    context = {'categories': categories, 'applyjobs': applyjobs}
    return render(request, 'jobs/jobgallery.html', context)

#view job

def viewJob(request, pk):
    applyjob = ApplyJob.objects.get(id=pk)
    return render(request, 'jobs/applyjob.html', {'applyjob': applyjob})


#job application ends.................

#galleryview
def jobgalleryview(request):
	jobs = Job.objects.all()
	context = {'jobs': jobs}
	template = 'jobs/joblistview.html'	
	return render(request, template, context)

#delete gallery image
def deleteJob(request, pk):
    jobs = Job.objects.get(id=pk)
    if len(jobs.image) > 0:
        os.remove(jobs.image.path)
    jobs.delete()
    messages.success(request,"Product Deleted Successfuly")
    return redirect('joblistview')

#jobcategory view
def JobCategoryView(request, category):
    user = request.user
    category_posts = Post.objects.filter(user=user)
    return render(request, 'job/category.html', { category_posts : category_posts})


# views.py
def job_detail(request, job_id):
    job = Job.objects.get(id=job_id)
    return render(request, 'jobs/job_detail.html', {'job': job})


