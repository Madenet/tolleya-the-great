from django.urls import path, include
from . import views 

urlpatterns = [
    path('send', views.send, name='send'),
    path('sendto_allcustomers', views.sendto_allcustomers, name='sendto_allcustomers'),
    path('sendto_activecustomers', views.sendto_activecustomers, name='sendto_activecustomers'),
    path('sendto_inactivecustomers', views.sendto_inactivecustomers, name='sendto_inactivecustomers'),
    path('custom_message', views.custom_message, name='custom_message'),
    path('add_customer/', views.add_customer, name='add_customer'),
]