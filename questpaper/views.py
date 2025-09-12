from main_app.models import Subject, Grade, Term, School
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from questpaper.models import QuestionPaper
from main_app.models import School, Grade, Term, Subject, Educator
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
import os
from django.conf import settings
from questpaper.forms import QuestionPaperUploadForm
from django.http import HttpResponse, FileResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import QuestionPaper,Topic, Department
from .forms import QuestionPaperUploadForm
from django.contrib import messages

# Upload Question Paper
def upload_question_paper(request):
    """Allow superusers to upload question papers without an educator."""

    if request.method == 'POST':
        form = QuestionPaperUploadForm(request.POST, request.FILES)

        if form.is_valid():
            # Create the question paper object but don't assign educator for superusers
            question_paper = form.save(commit=False)

            if not request.user.is_superuser:
                # Regular user - Assign educator (the user should be associated with an educator)
                educator = get_object_or_404(Educator, admin=request.user)
                question_paper.educator = educator

            # Save the question paper
            question_paper.save()
            form.save_m2m()  # Save ManyToMany relationships (topics)

            messages.success(request, "Question paper uploaded successfully.")
            return redirect('questionpaperlist')
        else:
            messages.error(request, "Failed to upload the question paper. Please check the form.")
    else:
        form = QuestionPaperUploadForm()

    return render(request, 'question_papers/upload.html', {'form': form})


#question papers
class QuestionPaperListView(ListView):
    model = QuestionPaper
    template_name = 'question_papers/question_paper_list.html'
    context_object_name = 'question_papers'


#question_paper_detail
def question_paper_detail(request, paper_id):
    paper = get_object_or_404(QuestionPaper, id=paper_id)
    
    # Check if the file is a PDF
    is_pdf = paper.file.url.lower().endswith('.pdf')

    return render(request, 'question_paper_detail.html', {'paper': paper, 'is_pdf': is_pdf})

# Filter Question Papers
def filter_question_papers(request):
    question_papers = QuestionPaper.objects.all()  # Fetch all question papers
    departments = Department.objects.all()  # Assuming a Department model exists
    grades = Grade.objects.all()
    terms = Term.objects.all()
    schools = School.objects.all()

    # You can leave out the filtering logic for now, as you want to display all question papers
    context = {
        'question_papers': question_papers,  # Display all question papers
        'departments': departments,
        'grades': grades,
        'terms': terms,
        'schools': schools,
    }
    return render(request, 'question_papers/questionpaperlist.html', context)


# Download Question Paper
def download_question_paper(request, pk):
    try:
        question_paper = QuestionPaper.objects.get(pk=pk)
        response = FileResponse(open(question_paper.file.path, 'rb'))
        return response
    except ObjectDoesNotExist:
        return HttpResponse("Question paper not found", status=404)
        

# View the Question Paper (instead of download)
def view_question_paper(request, pk):
    question_paper = get_object_or_404(QuestionPaper, pk=pk)

    # If the file is a PDF, render it in the browser
    file_path = question_paper.file.path

    if file_path.endswith('.pdf'):
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    else:
        return HttpResponse("This file format is not supported for viewing.", status=400)

# Topic Views
class TopicListView(ListView):
    model = Topic
    template_name = 'topic_list.html'  # Template to use
    context_object_name = 'topics'    # Context name in template

class TopicCreateView(CreateView):
    model = Topic
    fields = ['name']
    template_name = 'topic_form.html'  # Template for the form
    success_url = reverse_lazy('topic_list')  # Redirect after success

class TopicDetailView(DetailView):
    model = Topic
    template_name = 'topic_detail.html'
    context_object_name = 'topic'

class TopicUpdateView(UpdateView):
    model = Topic
    fields = ['name']
    template_name = 'topic_form.html'
    success_url = reverse_lazy('topic_list')

class TopicDeleteView(DeleteView):
    model = Topic
    template_name = 'topic_confirm_delete.html'  # Confirmation template
    success_url = reverse_lazy('topic_list')

# Department Views
class DepartmentListView(ListView):
    model = Department
    template_name = 'department_list.html'
    context_object_name = 'departments'

class DepartmentCreateView(CreateView):
    model = Department
    fields = ['name']
    template_name = 'department_form.html'
    success_url = reverse_lazy('department_list')

class DepartmentDetailView(DetailView):
    model = Department
    template_name = 'department_detail.html'
    context_object_name = 'department'

class DepartmentUpdateView(UpdateView):
    model = Department
    fields = ['name']
    template_name = 'department_form.html'
    success_url = reverse_lazy('department_list')

class DepartmentDeleteView(DeleteView):
    model = Department
    template_name = 'department_confirm_delete.html'
    success_url = reverse_lazy('department_list')