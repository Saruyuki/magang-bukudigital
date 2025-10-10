from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse

from .forms import TamuForm

# Create your views here.
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD_HASH = make_password('admin123')

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
        
        if username == ADMIN_USERNAME and check_password(password, ADMIN_PASSWORD_HASH):
            request.session['admin_logged_in'] = True
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            
    return render(request, 'login.html')
    
def logout_view(request):
    request.session.pop('logged_in', None)
    return redirect('login')
