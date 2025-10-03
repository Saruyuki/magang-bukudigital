from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('tamu/', views.tamu_form, name='tamu_form'),
    path('tamu/submit/', views.tamu_form, name='tamu_submit'),
    path('pegawai/', views.pegawai_form, name='pegawai_form'),
    path('pegawai/submit/', views.pegawai_form, name='pegawai_submit'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('tamu/list/', views.tamu_list_view, name='tamu_list'),
    path('pegawai/list/', views.pegawai_list_view, name='pegawai_list'),
]
