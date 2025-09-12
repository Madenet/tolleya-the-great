from django.views.generic import ListView
from .views import galleryview, AddUniversityView, UniversityView, addApplication, gallery, viewApplication, deleteApplication
from . import views
from django.urls import path

#applications
urlpatterns = [
    path('', views.gallery, name='applicationgallery'),
    path('application/<str:pk>/', views.viewApplication, name='application'),
    path('addapplication/', views.addApplication, name='addapplication'),
    path('listview/', views.galleryview, name='listview'),
    path('university/', views.UniversityView, name='universitys'),
    path('delete-application/<str:pk>', views.deleteApplication, name="delete-application"),
    path('adduniversity/', views.AddUniversityView, name='adduniversity'),
    
]