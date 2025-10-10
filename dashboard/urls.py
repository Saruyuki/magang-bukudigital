from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('tamu_list/', views.tamu_list_view, name='tamu_list'),
    path('pengurus_list/', views.pengurus_list_view, name='pengurus_list'),
]
