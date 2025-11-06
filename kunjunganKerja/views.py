from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden

from .models import Kunjungan
from .forms import KunjunganForm
from datetime import datetime

# Create your views here.

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

@login_required
def kunjungan_form(request, pk):
    kunjungan = get_object_or_404(Kunjungan, pk=pk)
    
    if (kunjungan.user != request.user) and not is_admin(request.user):
        return HttpResponseForbidden("Anda tidak memiliki akses ke form ini.")
    
    if request.method == 'POST':
        form = KunjunganForm(request.POST, request.FILES, instance=kunjungan, user=request.user)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.submitted_at = datetime.now()
            obj.foto_kunjungan = request.FILES.get('foto_kunjungan')
            lat = str(request.POST.get('client_lat')).replace(",", ".") or obj.foto_lat
            lon = str(request.POST.get('client_lon')).replace(",", ".") or obj.foto_lon
            obj.foto_datetime = request.POST.get('client_photo_dt') or obj.foto_datetime
            
            obj.foto_lat = float(lat)
            obj.foto_lon = float(lon)
            
            obj.save()
            return JsonResponse({'success': True})
        else :
            return JsonResponse({'success': False, 'errors': form.errors.as_json()})
    else:
        form = KunjunganForm(instance=kunjungan, user=request.user)
    return render(request, 'kunjungan_form.html', {'form': form})

