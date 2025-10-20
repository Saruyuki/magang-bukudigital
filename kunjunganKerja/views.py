from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden

from .models import Kunjungan
from .forms import KunjunganForm
from datetime import datetime

# Create your views here.

def is_admin(user):
    return user.role == 'admin'

@login_required
def kunjungan_form(request, pk):
    kunjungan = get_object_or_404(Kunjungan, pk=pk)
    
    if kunjungan.user != request.user and not request.user.role == 'admin' :
        return HttpResponseForbidden("Anda tidak memiliki akses ke form ini.")
    
    if request.method == 'POST':
        form = KunjunganForm(request.POST, request.FILES, instance=kunjungan, user=request.user)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.submitted_at = datetime.now()
            obj.foto_kegiatan = request.FILES.get('foto_kegiatan')
            obj.foto_lat = request.POST.get('client_lat') or obj.foto_lat
            obj.foto_lon = request.POST.get('client_lon') or obj.foto_lon
            obj.foto_datetime = request.POST.get('client_photo_dt') or obj.foto_datetime
            obj.save()
            return JsonResponse({'success': True})
        else :
            return JsonResponse({'success': False, 'errors': form.errors.as_json()})
    else:
        form = KunjunganForm(instance=kunjungan, user=request.user)
    return render(request, 'kunjungan_form.html', {'form': form})

