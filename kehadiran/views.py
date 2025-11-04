from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import KehadiranForm


@login_required
def kehadiran_form(request):
    if request.method == 'POST':
        form = KehadiranForm(request.POST, user=request.user)
        if form.is_valid():
            kehadiran = form.save(commit=False)
            
            kehadiran.nama = request.user.nama
            kehadiran.jabatan = request.user.jabatan

            try:
                kehadiran.save(commit=False)
                return JsonResponse({'success': True})
            except Exception as e:
                print(f"Error saving kehadiran: {e}")
                return JsonResponse({'success': False, 'error': 'Terjadi kesalahan saat menyimpan data'})
                
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})
                
    else:
        form = KehadiranForm(user=request.user)
        
    return render(request, 'kehadiran_form.html', {'form': form})
