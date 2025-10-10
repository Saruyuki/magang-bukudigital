from django.urls import path
from . import views

urlpatterns = [    
    path('', views.pengurus_form, name='pengurus_form'),
    path('submit/', views.pengurus_form, name='pengurus_submit'),
]
