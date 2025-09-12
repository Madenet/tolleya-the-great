from django.db import models
from django.shortcuts import render
import json
import requests
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, redirect, render)
from django.templatetags.static import static
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from main_app.models import School, Grade, Term, Subject, Educator
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
# Create your views here.
class Topic(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

#question paper
class QuestionPaper(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    
    # Make educator and subject fields nullable
    educator = models.ForeignKey(Educator, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    
    file = models.FileField(upload_to='question_papers/')
    
    # Restrict complexity_rating to values between 1-5
    COMPLEXITY_CHOICES = [(i, f"Level {i}") for i in range(1, 6)]
    complexity_rating = models.IntegerField(choices=COMPLEXITY_CHOICES)
    
    # Allow multiple topics
    topics = models.ManyToManyField(Topic, related_name="question_papers")
    
    number_of_questions = models.TextField()  # For storing question numbers, improve if structured data is needed

    def __str__(self):
        return f"{self.grade} - {self.term} - {self.subject.name}"
    

#Prospectors
class Prospectors(models.Model):
    institution = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    copy = models.FileField(upload_to='store/prospectors/')
    logo = models.ImageField(upload_to='store/prospectors/')

    def __str__(self):
        return self.filename

    def delete(self, *args, **kwargs):
        self.copy.delete()
        self.logo.delete()
        super().delete(*args, **kwargs)