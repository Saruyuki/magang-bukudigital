from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('tamu_list/', views.tamu_list_view, name='tamu_list'),
    path('pengurus_list/', views.pengurus_list_view, name='pengurus_list'),
    path('kunjungan_list', views.kunjungan_list_view, name='kunjungan_list'),
    path('surat/', views.surat_list_view, name="surat_list"),
    path('surat/upload/', views.surat_upload_view, name='upload_surat'),
    path('surat/debug/', views.surat_debug_pdfplumber, name='surat_debug_pdfplumber'),
    path('surat/debug/view/', views.surat_debug_page, name='surat_debug_page'),
]
