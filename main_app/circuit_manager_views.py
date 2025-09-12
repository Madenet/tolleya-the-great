import json
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (get_object_or_404, redirect, render)
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from .models import *

# Circuit Manager Home View
def circuit_manager_home(request):
    circuit_manager = get_object_or_404(Circuit_Manager, admin=request.user)
    items = NewsAndEvents.objects.all().order_by("-updated_date")
    total_students = Student.objects.filter(course=circuit_manager.course).count()
    total_educators = Educator.objects.count()
    total_subjects = Subject.objects.count()
    total_attendance = AttendanceReport.objects.filter(student__course=circuit_manager.course).count()

    context = {
        'page_title': 'Circuit Manager Dashboard',
        "title": "News & Events",
        "items": items,
        'total_students': total_students,
        'total_educators': total_educators,
        'total_subjects': total_subjects,
        'total_attendance': total_attendance,
    }
    return render(request, 'circuit_manager_template/home_content.html', context)


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


# Managing Attendance Reports
def circuit_manager_view_attendance_reports(request):
    circuit_manager = get_object_or_404(Circuit_Manager, admin=request.user)
    attendance_reports = AttendanceReport.objects.filter(student__course=circuit_manager.course)

    context = {
        'page_title': 'View Attendance Reports',
        'attendance_reports': attendance_reports,
    }
    return render(request, 'circuit_manager_template/view_attendance_reports.html', context)

def circuit_manager_add_attendance_report(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        status = request.POST.get('status')
        if student_id and status:
            AttendanceReport.objects.create(
                student=Student.objects.get(id=student_id),
                status=status
            )
            messages.success(request, "Attendance report added successfully!")
            return redirect(reverse('circuit_manager_view_attendance_reports'))
        else:
            messages.error(request, "Error adding attendance report. Please check the form.")
    
    students = Student.objects.all()
    context = {
        'page_title': 'Add Attendance Report',
        'students': students,
    }
    return render(request, 'circuit_manager_template/add_attendance_report.html', context)

def circuit_manager_edit_attendance_report(request, report_id):
    report = get_object_or_404(AttendanceReport, id=report_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status:
            report.status = status
            report.save()
            messages.success(request, "Attendance report updated successfully!")
            return redirect(reverse('circuit_manager_view_attendance_reports'))
        else:
            messages.error(request, "Error updating attendance report. Please check the form.")

    context = {
        'page_title': 'Edit Attendance Report',
        'report': report,
    }
    return render(request, 'circuit_manager_template/edit_attendance_report.html', context)

def circuit_manager_delete_attendance_report(request, report_id):
    report = get_object_or_404(AttendanceReport, id=report_id)
    if request.method == 'POST':
        report.delete()
        messages.success(request, "Attendance report deleted successfully!")
        return redirect(reverse('circuit_manager_view_attendance_reports'))

    context = {
        'page_title': 'Delete Attendance Report',
        'report': report,
    }
    return render(request, 'circuit_manager_template/delete_attendance_report.html', context)


# Managing Subjects
def circuit_manager_view_subjects(request):
    subjects = Subject.objects.all()

    context = {
        'page_title': 'View Subjects',
        'subjects': subjects,
    }
    return render(request, 'circuit_manager_template/view_subjects.html', context)

def circuit_manager_add_subject(request):
    form = SubjectForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            subject = form.save(commit=False)
            subject.save()
            messages.success(request, "Subject added successfully!")
            return redirect(reverse('circuit_manager_view_subjects'))
        else:
            messages.error(request, "Error adding subject. Please check the form.")
    
    context = {
        'form': form,
        'page_title': 'Add Subject',
    }
    return render(request, 'circuit_manager_template/add_subject.html', context)

def circuit_manager_edit_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    form = SubjectForm(request.POST or None, instance=subject)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Subject updated successfully!")
            return redirect(reverse('circuit_manager_view_subjects'))
        else:
            messages.error(request, "Error updating subject. Please check the form.")

    context = {
        'form': form,
        'page_title': 'Edit Subject',
    }
    return render(request, 'circuit_manager_template/edit_subject.html', context)

def circuit_manager_delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    if request.method == 'POST':
        subject.delete()
        messages.success(request, "Subject deleted successfully!")
        return redirect(reverse('circuit_manager_view_subjects'))

    context = {
        'subject': subject,
        'page_title': 'Delete Subject',
    }
    return render(request, 'circuit_manager_template/delete_subject.html', context)

# Managing Courses
def circuit_manager_view_courses(request):
    courses = Course.objects.all()

    context = {
        'page_title': 'View Courses',
        'courses': courses,
    }
    return render(request, 'circuit_manager_template/view_courses.html', context)

def circuit_manager_add_course(request):
    form = CourseForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            course = form.save(commit=False)
            course.save()
            messages.success(request, "Course added successfully!")
            return redirect(reverse('circuit_manager_view_courses'))
        else:
            messages.error(request, "Error adding course. Please check the form.")

    context = {
        'form': form,
        'page_title': 'Add Course',
    }
    return render(request, 'circuit_manager_template/add_course.html', context)

def circuit_manager_edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    form = CourseForm(request.POST or None, instance=course)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Course updated successfully!")
            return redirect(reverse('circuit_manager_view_courses'))
        else:
            messages.error(request, "Error updating course. Please check the form.")

    context = {
        'form': form,
        'page_title': 'Edit Course',
    }
    return render(request, 'circuit_manager_template/edit_course.html', context)

def circuit_manager_delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        course.delete()
        messages.success(request, "Course deleted successfully!")
        return redirect(reverse('circuit_manager_view_courses'))

    context = {
        'course': course,
        'page_title': 'Delete Course',
    }
    return render(request, 'circuit_manager_template/delete_course.html', context)

# Managing Sessions
def circuit_manager_view_sessions(request):
    sessions = Session.objects.all()

    context = {
        'page_title': 'View Sessions',
        'sessions': sessions,
    }
    return render(request, 'circuit_manager_template/view_sessions.html', context)

def circuit_manager_add_session(request):
    form = SessionForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            session = form.save(commit=False)
            session.save()
            messages.success(request, "Session added successfully!")
            return redirect(reverse('circuit_manager_view_sessions'))
        else:
            messages.error(request, "Error adding session. Please check the form.")

    context = {
        'form': form,
        'page_title': 'Add Session',
    }
    return render(request, 'circuit_manager_template/add_session.html', context)

def circuit_manager_edit_session(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    form = SessionForm(request.POST or None, instance=session)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Session updated successfully!")
            return redirect(reverse('circuit_manager_view_sessions'))
        else:
            messages.error(request, "Error updating session. Please check the form.")

    context = {
        'form': form,
        'page_title': 'Edit Session',
    }
    return render(request, 'circuit_manager_template/edit_session.html', context)

def circuit_manager_delete_session(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    if request.method == 'POST':
        session.delete()
        messages.success(request, "Session deleted successfully!")
        return redirect(reverse('circuit_manager_view_sessions'))

    context = {
        'session': session,
        'page_title': 'Delete Session',
    }
    return render(request, 'circuit_manager_template/delete_session.html', context)

# Managing Terms
def circuit_manager_view_terms(request):
    terms = Term.objects.all()

    context = {
        'page_title': 'View Terms',
        'terms': terms,
    }
    return render(request, 'circuit_manager_template/view_terms.html', context)

def circuit_manager_add_term(request):
    form = TermForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            term = form.save(commit=False)
            term.save()
            messages.success(request, "Term added successfully!")
            return redirect(reverse('circuit_manager_view_terms'))
        else:
            messages.error(request, "Error adding term. Please check the form.")

    context = {
        'form': form,
        'page_title': 'Add Term',
    }
    return render(request, 'circuit_manager_template/add_term.html', context)

def circuit_manager_edit_term(request, term_id):
    term = get_object_or_404(Term, id=term_id)
    form = TermForm(request.POST or None, instance=term)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Term updated successfully!")
            return redirect(reverse('circuit_manager_view_terms'))
        else:
            messages.error(request, "Error updating term. Please check the form.")

    context = {
        'form': form,
        'page_title': 'Edit Term',
    }
    return render(request, 'circuit_manager_template/edit_term.html', context)

def circuit_manager_delete_term(request, term_id):
    term = get_object_or_404(Term, id=term_id)
    if request.method == 'POST':
        term.delete()
        messages.success(request, "Term deleted successfully!")
        return redirect(reverse('circuit_manager_view_terms'))

    context = {
        'term': term,
        'page_title': 'Delete Term',
    }
    return render(request, 'circuit_manager_template/delete_term.html', context)

# Managing Students and Results as before
def circuit_manager_view_students(request):
    circuit_manager = get_object_or_404(Circuit_Manager, admin=request.user)
    students = Student.objects.filter(course=circuit_manager.course)

    context = {
        'page_title': 'View Students',
        'students': students,
    }
    return render(request, 'circuit_manager_template/view_students.html', context)

def circuit_manager_view_results(request):
    circuit_manager = get_object_or_404(Circuit_Manager, admin=request.user)
    results = StudentResult.objects.filter(student__course=circuit_manager.course)

    context = {
        'page_title': 'View Results',
        'results': results,
    }
    return render(request, 'circuit_manager_template/view_results.html', context)

# Continue with managing parents and members as in the previous implementation...

# Managing Parents
def circuit_manager_manage_parents(request):
    circuit_manager = get_object_or_404(Circuit_Manager, admin=request.user)
    parents = Parent.objects.filter(student__course=circuit_manager.course)

    context = {
        'page_title': 'Manage Parents',
        'parents': parents,
    }
    return render(request, 'circuit_manager_template/manage_parents.html', context)

def circuit_manager_add_parent(request):
    form = ParentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            parent = form.save(commit=False)
            parent.save()
            messages.success(request, "Parent added successfully!")
            return redirect(reverse('circuit_manager_manage_parents'))
        else:
            messages.error(request, "Error adding parent. Please check the form.")
    
    context = {
        'form': form,
        'page_title': 'Add Parent',
    }
    return render(request, 'circuit_manager_template/add_parent.html', context)

def circuit_manager_edit_parent(request, parent_id):
    parent = get_object_or_404(Parent, id=parent_id)
    form = ParentForm(request.POST or None, instance=parent)
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Parent details updated successfully!")
            return redirect(reverse('circuit_manager_manage_parents'))
        else:
            messages.error(request, "Error updating parent. Please check the form.")
    
    context = {
        'form': form,
        'page_title': 'Edit Parent',
    }
    return render(request, 'circuit_manager_template/edit_parent.html', context)

def circuit_manager_delete_parent(request, parent_id):
    parent = get_object_or_404(Parent, id=parent_id)
    if request.method == 'POST':
        parent.delete()
        messages.success(request, "Parent deleted successfully!")
        return redirect(reverse('circuit_manager_manage_parents'))
    
    context = {
        'parent': parent,
        'page_title': 'Delete Parent',
    }
    return render(request, 'circuit_manager_template/delete_parent.html', context)

# Managing Members
def circuit_manager_manage_members(request):
    members = Member.objects.all()  # Adjust based on the context needed for Circuit Managers
    
    context = {
        'page_title': 'Manage Members',
        'members': members,
    }
    return render(request, 'circuit_manager_template/manage_members.html', context)

def circuit_manager_add_member(request):
    form = MemberForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            member = form.save(commit=False)
            member.save()
            messages.success(request, "Member added successfully!")
            return redirect(reverse('circuit_manager_manage_members'))
        else:
            messages.error(request, "Error adding member. Please check the form.")
    
    context = {
        'form': form,
        'page_title': 'Add Member',
    }
    return render(request, 'circuit_manager_template/add_member.html', context)

def circuit_manager_edit_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    form = MemberForm(request.POST or None, instance=member)
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Member details updated successfully!")
            return redirect(reverse('circuit_manager_manage_members'))
        else:
            messages.error(request, "Error updating member. Please check the form.")
    
    context = {
        'form': form,
        'page_title': 'Edit Member',
    }
    return render(request, 'circuit_manager_template/edit_member.html', context)

def circuit_manager_delete_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    if request.method == 'POST':
        member.delete()
        messages.success(request, "Member deleted successfully!")
        return redirect(reverse('circuit_manager_manage_members'))
    
    context = {
        'member': member,
        'page_title': 'Delete Member',
    }
    return render(request, 'circuit_manager_template/delete_member.html', context)
