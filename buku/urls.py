from django.urls import path
from . import views

urlpatterns = [
    path('', views.tamu_form, name='tamu_form'),
    path('submit/', views.tamu_form, name='tamu_submit'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
