from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('api/auth/login/', views.CustomTokenObtainPairView.as_view()),
    path('api/auth/refresh/', TokenRefreshView.as_view()),
    path('api/messages/', views.messages_view),
    path('api/messages/<int:message_id>/like/', views.message_like_view),
    path('api/upload/', views.upload_file_view),
    path('api/projects/', views.ProjectListCreateView.as_view()),
]
