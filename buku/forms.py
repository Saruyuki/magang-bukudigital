from django import forms
from .models import Tamu
from dashboard.utils import INDO_PROVINCES

class TamuForm(forms.ModelForm):
    provinsi = forms.ChoiceField(
        choices=[('', 'Pilih Provinsi')] + INDO_PROVINCES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Provinsi'
    )
    
    class Meta:
        model = Tamu
        fields = ['instansi', 'nama', 'phone', 'email', 'provinsi', 'kota', 'keperluan']
        widgets = {
            'instansi': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Instansi'}),
            'nama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Lengkap'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nomor Telepon'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email (opsional)'}),
            'kota': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kabupaten/Kota'}),
            'keperluan': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Keperluan Anda', 'rows': 3}),
        }
        labels = {
            'nama': 'Nama Lengkap',
            'phone': 'Nomor Telepon',
            'email': 'Email (opsional)',
            'provinsi': 'Provinsi',
            'kota': 'Kabupaten/Kota',
            'keperluan': 'Keperluan',
        }
        