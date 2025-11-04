from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from django.utils import timezone

from kunjunganKerja.models import Kunjungan

from datetime import date

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.role == 'pengurus':
                return redirect('profile')
            elif user.role == 'admin':
                return redirect('admin_dashboard')
            
        else:
            messages.error(request, 'Username atau password salah.')
        
    return render(request, 'login.html')
    
def logout_view(request):
    request.session.pop('logged_in', None)
    return redirect('login')

def profile_view(request):
    today = date.today()
    user = request.user
    kunjungan_list = Kunjungan.objects.filter(
        user=user,
        tanggal_kunjungan__gte=today
        ).order_by('tanggal_kunjungan')
    
    return render(request, 'profile.html', {
        'user': user,
        'kunjungan_list': kunjungan_list,
    })
            
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': form.errors.as_json()})
    return JsonResponse({'success': False, 'error': 'Invalid request'})



