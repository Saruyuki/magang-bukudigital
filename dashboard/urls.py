from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('tamu_list/', views.tamu_list_view, name='tamu_list'),
    path('pengurus_list/', views.pengurus_list_view, name='pengurus_list'),
    path('kunjungan_list/', views.kunjungan_list_view, name='kunjungan_list'),
    path('surat/', views.surat_list_view, name="surat_list"),
    path('surat/upload/', views.surat_upload_view, name='upload_surat'),
    path('surat/debug/', views.surat_debug_pdfplumber, name='surat_debug_pdfplumber'),
    path('surat/debug/view/', views.surat_debug_page, name='surat_debug_page'),
    path('surat/<int:surat_id>/delete', views.surat_delete_view, name='delete_surat'),
    path('surat/<int:surat_id>/edit', views.surat_edit_view, name='edit_surat'),
    path('surat/<int:surat_id>/show', views.surat_show_view, name='show_surat'),
    path('user/', views.user_list, name='user_list'),
    path('user/<int:pk>/edit/', views.edit_user, name='edit_user'),
    path('user/<int:pk>/delete/', views.delete_user, name='delete_user'),
]
