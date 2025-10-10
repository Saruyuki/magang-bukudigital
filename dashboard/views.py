from django.shortcuts import render, redirect
from django.utils.timezone import now
from buku.models import Tamu
from kehadiran.models import Pengurus
from .utils import categorize_keperluan, PROVINCE_ACRONYMS

import pandas as pd

# Create your views here.

def admin_dashboard(request):
    if not request.session.get('admin_logged_in'):
        return redirect('login')
    
    today = now().date()
    start_of_month = today.replace(day=1)
    
    tamu_qs = Tamu.objects.filter(tanggal_kunjungan__date__gte=start_of_month)
    tamu_today =tamu_qs.filter(tanggal_kunjungan__date=today)
    
    df_tamu = pd.DataFrame(list(tamu_qs.values()))
    df_tamu_today = pd.DataFrame(list(tamu_today.values()))
    
    pengunjung_bulan = len(df_tamu) if not df_tamu.empty else 0
    pengunjung_hari = len(df_tamu_today) if not df_tamu_today.empty else 0
    
    provinsi_terbanyak = df_tamu['provinsi'].value_counts().to_dict()
    provinsi_labels = list(provinsi_terbanyak.keys())
    provinsi_data = list(provinsi_terbanyak.values())
    
    provinsi_labels_acronym = [PROVINCE_ACRONYMS.get(prov, prov) for prov in provinsi_labels]
    
    if not df_tamu.empty:
        df_tamu['keperluan_kategori'] = df_tamu['keperluan'].apply(lambda x: categorize_keperluan(x))
        banyak_keperluan = df_tamu['keperluan_kategori'].value_counts().to_dict()        
      
    keperluan_labels = list(banyak_keperluan.keys())
    keperluan_data = list(banyak_keperluan.values())
    
    pengurus_today = Pengurus.objects.filter(tanggal_masuk__date=today)
    pengurus_hari = pengurus_today.count()
    
    return render(request, 'admin_dashboard.html', {
        'pengunjung_bulan': pengunjung_bulan,
        'pengunjung_hari': pengunjung_hari,
        'pengurus_hari': pengurus_hari,
        'provinsi_labels': provinsi_labels_acronym,
        'provinsi_data': provinsi_data,
        'keperluan_labels': keperluan_labels,
        'keperluan_data': keperluan_data,
    })

def tamu_list_view(request):
    if not request.session.get('admin_logged_in'):
        return redirect('login')
    
    tamu_list = Tamu.objects.all().order_by('-tanggal_kunjungan')
    return render(request, 'tamu_list.html', {'tamu_list': tamu_list})

def pengurus_list_view(request):
    if not request.session.get('admin_logged_in'):
        return redirect('login')
    
    pengurus_list = Pengurus.objects.all().order_by('-tanggal_masuk')
    return render(request, 'pengurus_list.html', {'pengurus_list': pengurus_list})
    