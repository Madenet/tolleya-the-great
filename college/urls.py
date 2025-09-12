from django.urls import path
from .views import college_list_view, college_add_view, college_update_view, college_delete_view, college_detail

urlpatterns = [
    path('colleges/', college_list_view, name='college_list'),
    path('colleges/add/', college_add_view, name='college_add'),
    path('colleges/update/<int:pk>/', college_update_view, name='college_update'),
    path('colleges/delete/<int:pk>/', college_delete_view, name='college_delete'),
    path('college/<int:pk>/', college_detail, name='college_detail'),

]
