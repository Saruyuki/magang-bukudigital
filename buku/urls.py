from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('tamu/', views.tamu_form, name='tamu_form'),
    path('tamu/submit/', views.tamu_form, name='tamu_submit'),
    path('tamu_legacy/', views.tamu_legacy, name="tamu_legacy"),    
    path('pengurus/', views.pengurus_form, name='pengurus_form'),
    path('pengurus/submit/', views.pengurus_form, name='pengurus_submit'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('tamu/list/', views.tamu_list_view, name='tamu_list'),
    path('pengurus/list/', views.pengurus_list_view, name='pengurus_list'),
]
