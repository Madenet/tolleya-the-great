from django.urls import path
from . import views
from django.views.generic import ListView
from .views import galleryview, addPhoto, gallery, viewPhoto, deletePhoto, CategoryView, approve_photos

#GalleryView
urlpatterns = [ 
    path('', views.gallery, name='gallery'),
    path('photo/<str:pk>/', views.viewPhoto, name='photo'),
    path('add/', views.addPhoto, name='add'),
    path('approve_photos/', views.approve_photos, name='approve_photos'),
    path('photo/edit/<int:pk>/', views.edit_photo, name='edit_photo'),
    path('listview/', views.galleryview, name='listview'),
    path('delete-photo/<str:pk>', views.deletePhoto, name="delete-photo"),
    path('category/<str:cats>/', views.CategoryView, name='category'),
]
