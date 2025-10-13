from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
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

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Username atau password salah.')
        
    return render(request, 'login.html')
    
def logout_view(request):
    request.session.pop('logged_in', None)
    return redirect('login')
