from django.urls import path
from . import views

urlpatterns = [    
    path('', views.kehadiran_form, name='kehadiran_form'),
    path('submit/', views.kehadiran_form, name='kehadiran_submit'),
]
