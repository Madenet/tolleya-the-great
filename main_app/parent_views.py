from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from .forms import *

# Parent Home
def parent_home(request):
    parent = get_object_or_404(Parent, admin=request.user)
    students = parent.student.all()  # Get all linked students

    total_attendance_reports = AttendanceReport.objects.filter(student__in=students).count()
    items = NewsAndEvents.objects.all().order_by("-updated_date")

    context = {
        "title": "News & Events",
        "items": items,
        'page_title': 'Parent Dashboard',
        'total_attendance_reports': total_attendance_reports,
        'students': students,  # Pass to template
        'parent': parent,
    }
    return render(request, 'parent_template/home_content.html', context)

# View Attendance Reports
def parent_view_attendance(request):
    parent = get_object_or_404(Parent, admin=request.user)
    attendance_reports = AttendanceReport.objects.filter(student=parent.student)

    context = {
        'page_title': 'Attendance Reports',
        'attendance_reports': attendance_reports,
    }
    return render(request, 'parent_template/view_attendance.html', context)

# View Profile
def parent_view_profile(request):
    parent = get_object_or_404(Parent, admin=request.user)
    
    if request.method == 'POST':
        # Updating directly on the model, no form
        parent.school = request.POST.get('school', parent.school)
        parent.grade = request.POST.get('grade', parent.grade)
        parent.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('parent_view_profile')

    context = {
        'page_title': 'Profile',
        'parent': parent,
    }
    return render(request, 'parent_template/view_profile.html', context)

# Manage Attendance Reports
def parent_manage_attendance_reports(request):
    parent = get_object_or_404(Parent, admin=request.user)
    attendance_reports = AttendanceReport.objects.filter(student=parent.student)

    context = {
        'page_title': 'Manage Attendance Reports',
        'attendance_reports': attendance_reports,
    }
    return render(request, 'parent_template/manage_attendance_reports.html', context)

# Add Attendance Report
def parent_add_attendance_report(request):
    parent = get_object_or_404(Parent, admin=request.user)

    if request.method == 'POST':
        # Creating attendance report directly from POST data
        AttendanceReport.objects.create(
            student=parent.student,
            attendance_id=request.POST.get('attendance_id'),
            status=bool(request.POST.get('status', False))
        )
        messages.success(request, "Attendance report added successfully!")
        return redirect('parent_manage_attendance_reports')

    context = {
        'page_title': 'Add Attendance Report',
    }
    return render(request, 'parent_template/add_attendance_report.html', context)

# Edit Attendance Report
def parent_edit_attendance_report(request, report_id):
    report = get_object_or_404(AttendanceReport, id=report_id)

    if request.method == 'POST':
        report.attendance_id = request.POST.get('attendance_id', report.attendance_id)
        report.status = bool(request.POST.get('status', report.status))
        report.save()
        messages.success(request, "Attendance report updated successfully!")
        return redirect('parent_manage_attendance_reports')

    context = {
        'page_title': 'Edit Attendance Report',
        'report': report,
    }
    return render(request, 'parent_template/edit_attendance_report.html', context)

# Delete Attendance Report
def parent_delete_attendance_report(request, report_id):
    report = get_object_or_404(AttendanceReport, id=report_id)
    if request.method == 'POST':
        report.delete()
        messages.success(request, "Attendance report deleted successfully!")
        return redirect('parent_manage_attendance_reports')

    context = {
        'page_title': 'Delete Attendance Report',
        'report': report,
    }
    return render(request, 'parent_template/delete_attendance_report.html', context)
