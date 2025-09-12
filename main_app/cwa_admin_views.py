from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from .forms import *

#cwa admin
def cwa_admin_home(request):
    return render(request, 'cwa_admin_template/home_content.html', {
        'page_title': 'CWA Admin Dashboard'
    })