# urls.py
from django.urls import path
from .views import bursary_list_view, bursary_add_view, bursary_update_view, bursary_delete_view ,bursary_detail

urlpatterns = [
    path('bursaries/', bursary_list_view, name='bursary_list'),
    path('bursaries/add/', bursary_add_view, name='bursary_add'),
    path('bursaries/update/<int:pk>/', bursary_update_view, name='bursary_update'),
    path('bursaries/delete/<int:pk>/', bursary_delete_view, name='bursary_delete'),
    path('bursary/<int:pk>/', bursary_detail, name='bursary_detail'),

]
