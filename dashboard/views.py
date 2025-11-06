from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import  user_passes_test, login_required
from django.views.decorators.http import require_POST
from django.utils.timezone import now
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.db import transaction

from datetime import timedelta

from accounts.models import CustomUser
from kunjunganKerja.models import Surat, Kunjungan

from kehadiran.models import Kehadiran
from buku.models import Tamu

from .utils import categorize_keperluan, PROVINCE_ACRONYMS, parse_surat_tugas
from .forms import SingleUserForm, BulkUserUploadForm

import pandas as pd
import pdfplumber

User = get_user_model()

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    
    today = now().date()
    start_of_month = today.replace(day=1)
    
    tamu_qs = Tamu.objects.filter(tanggal_kunjungan__date__gte=start_of_month)
    tamu_today =tamu_qs.filter(tanggal_kunjungan__date=today)
    
    df_tamu = pd.DataFrame(list(tamu_qs.values()))
    df_tamu_today = pd.DataFrame(list(tamu_today.values()))
    
    pengunjung_bulan = len(df_tamu) if not df_tamu.empty else 0
    pengunjung_hari = len(df_tamu_today) if not df_tamu_today.empty else 0
        
    provinsi_labels_acronym = []
    provinsi_data = []
    keperluan_labels = []
    keperluan_data = []
        
    if not df_tamu.empty:
        if 'provinsi' in df_tamu.columns:
            provinsi_terbanyak = df_tamu['provinsi'].value_counts().to_dict()
            provinsi_labels = list(provinsi_terbanyak.keys())
            provinsi_data = list(provinsi_terbanyak.values())
            
            provinsi_labels_acronym = [PROVINCE_ACRONYMS.get(prov, prov) for prov in provinsi_labels]
        
        if 'keperluan' in df_tamu.columns:
            df_tamu['keperluan_kategori'] = df_tamu['keperluan'].apply(lambda x: categorize_keperluan(x))
            banyak_keperluan = df_tamu['keperluan_kategori'].value_counts().to_dict()        
      
            keperluan_labels = list(banyak_keperluan.keys())
            keperluan_data = list(banyak_keperluan.values())
    
    pengurus_today = Kehadiran.objects.filter(tanggal_masuk__date=today)
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

@login_required
@user_passes_test(is_admin)
def tamu_list_view(request):   
    tamu_list = Tamu.objects.all().order_by('-tanggal_kunjungan')
    return render(request, 'tamu_list.html', {'tamu_list': tamu_list})

@login_required
def pengurus_list_view(request):   
    pengurus_list = Kehadiran.objects.all().order_by('-tanggal_masuk')
    return render(request, 'pengurus_list.html', {'pengurus_list': pengurus_list})

@login_required
def kunjungan_list_view(request):
    user = request.user
    
    if user.role == 'admin':
        kunjungan_list = Kunjungan.objects.select_related('user', 'surat').order_by('-tanggal_kunjungan')
    else :
        kunjungan_list = Kunjungan.objects.filter(user=user).select_related('surat').order_by('-tanggal_kunjungan')        
    
    return render(request, 'kunjungan_list.html', {
        'kunjungan_list': kunjungan_list,
        'is_admin': user.role == 'admin',
        })
    
@user_passes_test(is_admin)
def surat_list_view(request):
    surat_list = Surat.objects.all().order_by('-created_at')
    return render(request, 'surat_list.html', {'surat_list': surat_list})

@user_passes_test(is_admin)
def surat_upload_view(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    
    file = request.FILES['file']
    if not file:
        return JsonResponse({'success': False, 'error': 'File tidak ditemukan'})
    
    print(file.size)
    
    try: 
        surat_data = parse_surat_tugas(file)
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Gagal memproses file: {e}'})
    
    print(file.size)
    
    if not surat_data or not surat_data['no_surat']:
        return JsonResponse({'success': False, 'error': 'Gagal membaca format surat'})
    
    if request.GET.get('preview') == 'true':
        return JsonResponse({'success': True, 'mode': 'preview', 'parsed': surat_data})
    
    try :
        with transaction.atomic():
            surat = Surat.objects.create(
                no_surat=surat_data['no_surat'],
                file=file,
                uploaded_by=request.user
            )

        start = surat_data['start_date']
        end = surat_data['end_date']
        pengurus = surat_data['pengurus']
        tujuan = surat_data['tujuan']
        agenda = surat_data['agenda']
        
        print("Parsed Data:", surat_data)
        print("Creating Kunjungan between", start, 'and', end)
        print("Pengurus:", pengurus)
        
        created_count = 0
        if start and end and pengurus:
            for offset in range((end - start).days + 1):
                tanggal = start + timedelta (days=offset)
                for nama, jabatan in pengurus:
                    user = CustomUser.objects.filter(nama__iexact=nama).first()
                    if not user:
                        continue
                    Kunjungan.objects.create(
                        surat=surat,
                        user=user,
                        no_surat=surat_data['no_surat'],
                        nama=nama,
                        jabatan=jabatan,
                        tujuan=tujuan,
                        agenda=agenda,
                        tanggal_kunjungan=tanggal,
                    )
                    created_count += 1
                    
        return JsonResponse({'success': True, 'created': created_count})
    except Exception as e:
        print("Upload error:", e)
        return JsonResponse({'success': False, 'error': f'Kesalahan server: {e}'})

@user_passes_test(is_admin)
@require_POST
def surat_delete_view(request, surat_id):
    surat = get_object_or_404(Surat, id=surat_id)
    surat.delete()
    return JsonResponse({'success': True})

@user_passes_test(is_admin)
@require_POST
def surat_edit_view(request, surat_id):
    surat = get_object_or_404(Surat, id=surat_id)
    new_no = request.POST.get('no_surat')
    if not new_no:
        return JsonResponse({'success': False, 'error': 'Nomor surat tidak boleh kosong'})
    surat.no_surat = new_no
    surat.save()
    return JsonResponse({'success': True, 'no_surat': surat.no_surat})

@user_passes_test(is_admin)
def surat_show_view(request, surat_id):
    surat = get_object_or_404(Surat, id=surat_id)
    if not surat.file:
        return HttpResponse("Tidak ada file diunggah", content_type="text/plain")
    return redirect(surat.file.url)

    
@user_passes_test(is_admin)
def surat_debug_pdfplumber(request):
    """
    Debug endpoint to show what pdfplumber actually extracts from a Surat PDF.
    Uploads a PDF and returns the extracted text and line structure.
    """
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        result = {}

        try:
            with pdfplumber.open(file) as pdf:
                pages_data = []
                for page_number, page in enumerate(pdf.pages, start=1):
                    text = page.extract_text() or ""
                    lines = text.splitlines() if text else []
                    words = page.extract_words()
                    pages_data.append({
                        "page": page_number,
                        "line_count": len(lines),
                        "lines": lines,
                        "words_count": len(words),
                        "first_words": [w["text"] for w in words[:20]],  # show first 20 words
                    })

                result["pages"] = pages_data
                result["success"] = True
                result["page_count"] = len(pdf.pages)
        except Exception as e:
            result = {"success": False, "error": str(e)}

        return JsonResponse(result, json_dumps_params={"ensure_ascii": False, "indent": 2})

    return JsonResponse({"success": False, "error": "Gunakan POST dengan file PDF"})

@user_passes_test(is_admin)
def surat_debug_page(request):
    return render(request, 'debug_pdfplumber.html')

@login_required
@user_passes_test(is_admin)
def user_list(request):
    single_form = SingleUserForm()
    bulk_form = BulkUserUploadForm()
    
    if request.method == 'POST':
        if 'single_submit' in request.POST:
            single_form = SingleUserForm(request.POST)
            if single_form.is_valid():
                single_form.save()
                messages.success(request, 'User berhasil ditambahkan.')
                return redirect('user_list')
            
        elif 'bulk_submit' in request.POST:
            bulk_form = BulkUserUploadForm(request.POST, request.FILES)
            if bulk_form.is_valid():
                file = request.FILES['file']
                try:
                    if file.name.endswith('.csv'):
                        df = pd.read_csv(file)
                    else:
                        df = pd.read_excel(file)
                        
                    for _, row in df.iterrows():
                        username = str(row['username']).strip()
                        password = str(row['password']).strip()
                        nama = str(row.get('nama', '')).strip()
                        jabatan = str(row.get('jabatan', '')).strip()
                        role = str(row.get('role', 'pengurus')).strip()
                        
                        if not User.objects.filter(username=username).exists():
                            user = User(username=username, nama=nama, jabatan=jabatan, role=role)
                            user.set_password(password)
                            user.save()
                            
                    messages.success(request, 'Data pengguna berhasil diunggah.')
                    return redirect('user_list')
                
                except Exception as e:
                    messages.error(request, f"Terjadi kesalahan: {e}")
                    
    users = User.objects.all()
    return render(request, 'user_list.html', {
        'single_form': single_form,
        'bulk_form': bulk_form,
        'users': users,
    })
    
@login_required
@user_passes_test(is_admin)
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        nama = request.POST.get('editNama')
        jabatan = request.POST.get('editJabatan')
        role = request.POST.get('editRole')
        
        if not nama or not jabatan or not role:
            return JsonResponse({'success': False, 'error': 'Semua field wajib diisi.'})
        
        user.nama = nama
        user.jabatan = jabatan
        user.role = role
        
        user.save()
        
        return JsonResponse({'success': True})
    
    return JsonResponse({
        'id': user.id,
        'nama': user.nama,
        'jabatan': user.jabatan,
        'role': user.role,
    })
    
@login_required
@user_passes_test(is_admin)
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    if user == request.user:
        return JsonResponse({'success': False, 'error': 'Anda tidak dapat menghapus akun Anda sendiri.'})
    
    if request.method =='POST':
        user.delete()
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': 'Permintaan tidak valid.'})