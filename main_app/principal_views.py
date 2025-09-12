import json
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponseRedirect, get_object_or_404, redirect, render)
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .forms import *
from .models import *


#principal home
def principal_home(request):
    principal = get_object_or_404(Principal, admin=request.user)
    
    # Filter news based on school name appearing in title or summary
    items = NewsAndEvents.objects.filter(
        Q(title__icontains=principal.school.name) | 
        Q(summary__icontains=principal.school.name)
    ).order_by("-updated_date")

    total_students = Student.objects.filter(school=principal.school).count()
    total_educators = Educator.objects.filter(school=principal.school).count()
    total_subjects = Subject.objects.filter(course_id__school=principal.school).count()
    total_attendance = AttendanceReport.objects.filter(student__school=principal.school).count()

    context = {
        'page_title': 'Principal Dashboard',
        "title": "News & Events",
        "items": items,
        'total_students': total_students,
        'total_educators': total_educators,
        'total_subjects': total_subjects,
        'total_attendance': total_attendance
    }
    return render(request, 'principal_template/home_content.html', context)


def post_add(request):
    if request.method == "POST":
        form = NewsAndEventsForm(request.POST)
        title = request.POST.get("title")
        if form.is_valid():
            form.save()

            messages.success(request, (title + " has been uploaded."))
            return redirect("admin_home")
        else:
            messages.error(request, "Please correct the error(s) below.")
    else:
        form = NewsAndEventsForm()
    return render(
        request,
        "hod_template/post_add.html",
        {
            "title": "Add Post",
            "form": form,
        },
    )



def edit_post(request, pk):
    instance = get_object_or_404(NewsAndEvents, pk=pk)
    if request.method == "POST":
        form = NewsAndEventsForm(request.POST, instance=instance)
        title = request.POST.get("title")
        if form.is_valid():
            form.save()

            messages.success(request, (title + " has been updated."))
            return redirect("home")
        else:
            messages.error(request, "Please correct the error(s) below.")
    else:
        form = NewsAndEventsForm(instance=instance)
    return render(
        request,
        "hod_template/post_add.html",
        {
            "title": "Edit Post",
            "form": form,
        },
    )



def delete_post(request, pk):
    post = get_object_or_404(NewsAndEvents, pk=pk)
    title = post.title
    post.delete()
    messages.success(request, (title + " has been deleted."))
    return redirect("staff_home")

def principal_view_results(request):
    principal = get_object_or_404(Principal, admin=request.user)
    results = StudentResult.objects.filter(student__course=principal.course)
    
    context = {
        'page_title': 'View Results',
        'results': results
    }
    return render(request, 'principal_template/view_results.html', context)

def principal_view_attendance(request):
    principal = get_object_or_404(Principal, admin=request.user)
    attendance_reports = AttendanceReport.objects.filter(student__course=principal.course)
    
    context = {
        'page_title': 'View Attendance',
        'attendance_reports': attendance_reports
    }
    return render(request, 'principal_template/view_attendance.html', context)

def principal_view_educators(request):
    principal = get_object_or_404(Principal, admin=request.user)
    educators = Educator.objects.all()
    
    context = {
        'page_title': 'View Educators',
        'educators': educators
    }
    return render(request, 'principal_template/view_educators.html', context)

def principal_view_profile(request):
    principal = get_object_or_404(Principal, admin=request.user)
    form = PrincipalEditForm(request.POST or None, request.FILES or None, instance=principal)
    
    context = {
        'form': form,
        'page_title': 'View/Update Profile'
    }
    
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('principal_view_profile'))
            except Exception as e:
                messages.error(request, "Could not update profile!")
        else:
            messages.error(request, "Invalid data!")
    
    return render(request, 'principal_template/view_profile.html', context)

def principal_view_attendance_report(request):
    principal = get_object_or_404(Principal, admin=request.user)
    attendance_reports = AttendanceReport.objects.filter(student__course=principal.course)
    
    context = {
        'page_title': 'Attendance Reports',
        'attendance_reports': attendance_reports
    }
    return render(request, 'principal_template/view_attendance_reports.html', context)

def principal_view_student_results(request):
    principal = get_object_or_404(Principal, admin=request.user)
    student_results = StudentResult.objects.filter(student__course=principal.course)
    
    context = {
        'page_title': 'Student Results',
        'student_results': student_results
    }
    return render(request, 'principal_template/view_student_results.html', context)

@csrf_exempt
def fetch_student_attendance(request):
    try:
        student_id = request.POST.get('student_id')
        attendance_data = AttendanceReport.objects.filter(student_id=student_id)
        attendance_list = [
            {
                'date': attendance.attendance.date,
                'status': attendance.status
            } for attendance in attendance_data
        ]
        return JsonResponse(attendance_list, safe=False)
    except Exception as e:
        return HttpResponse('Error: ' + str(e))

@csrf_exempt
def fetch_student_results(request):
    try:
        student_id = request.POST.get('student_id')
        results_data = StudentResult.objects.filter(student_id=student_id)
        results_list = [
            {
                'exam': result.exam,
                'assignment': result.assignment,
                'test': result.test,
                'subject': result.subject.name
            } for result in results_data
        ]
        return JsonResponse(results_list, safe=False)
    except Exception as e:
        return HttpResponse('Error: ' + str(e))


def principal_manage_parents(request):
    principal = get_object_or_404(Principal, admin=request.user)
    parents = Parent.objects.filter(student__course=principal.course)

    context = {
        'page_title': 'Manage Parents',
        'parents': parents
    }
    return render(request, 'principal_template/manage_parents.html', context)


def principal_add_parent(request):
    form = ParentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            parent = form.save(commit=False)
            parent.save()
            messages.success(request, "Parent added successfully!")
            return redirect(reverse('principal_manage_parents'))
        else:
            messages.error(request, "Error adding parent. Please check the form.")
    
    context = {
        'form': form,
        'page_title': 'Add Parent'
    }
    return render(request, 'principal_template/add_parent.html', context)

def principal_edit_parent(request, parent_id):
    parent = get_object_or_404(Parent, id=parent_id)
    form = ParentForm(request.POST or None, instance=parent)
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Parent details updated successfully!")
            return redirect(reverse('principal_manage_parents'))
        else:
            messages.error(request, "Error updating parent. Please check the form.")
    
    context = {
        'form': form,
        'page_title': 'Edit Parent'
    }
    return render(request, 'principal_template/edit_parent.html', context)

def principal_delete_parent(request, parent_id):
    parent = get_object_or_404(Parent, id=parent_id)
    if request.method == 'POST':
        parent.delete()
        messages.success(request, "Parent deleted successfully!")
        return redirect(reverse('principal_manage_parents'))
    
    context = {
        'parent': parent,
        'page_title': 'Delete Parent'
    }
    return render(request, 'principal_template/delete_parent.html', context)

def principal_manage_members(request):
    members = Member.objects.all()  # Or filter based on the principal's school
    
    context = {
        'page_title': 'Manage Members',
        'members': members
    }
    return render(request, 'principal_template/manage_members.html', context)

def principal_add_member(request):
    form = MemberForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            member = form.save(commit=False)
            member.save()
            messages.success(request, "Member added successfully!")
            return redirect(reverse('principal_manage_members'))
        else:
            messages.error(request, "Error adding member. Please check the form.")
    
    context = {
        'form': form,
        'page_title': 'Add Member'
    }
    return render(request, 'principal_template/add_member.html', context)

def principal_edit_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    form = MemberForm(request.POST or None, instance=member)
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Member details updated successfully!")
            return redirect(reverse('principal_manage_members'))
        else:
            messages.error(request, "Error updating member. Please check the form.")
    
    context = {
        'form': form,
        'page_title': 'Edit Member'
    }
    return render(request, 'principal_template/edit_member.html', context)

def principal_delete_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    if request.method == 'POST':
        member.delete()
        messages.success(request, "Member deleted successfully!")
        return redirect(reverse('principal_manage_members'))
    
    context = {
        'member': member,
        'page_title': 'Delete Member'
    }
    return render(request, 'principal_template/delete_member.html', context)