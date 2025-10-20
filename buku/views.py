from django.shortcuts import render, redirect
from django.http import JsonResponse

from .forms import TamuForm

# Create your views here.
def tamu_form(request):
    if request.method == 'POST':
        form = TamuForm(request.POST)
        if form.is_valid():
            tamu = form.save(commit=False)
            try:
                tamu.save()
                return JsonResponse({'success': True})
            except Exception as e:
                print(f"Error saving tamu: {e}")
                return JsonResponse({'success': False, 'error': 'Terjadi kesalahan saat menyimpan data.'})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})
                
    else:
        form = TamuForm()
    return render(request, 'tamu_form.html', {'form': form})
