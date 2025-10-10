from django import forms
from .models import Pengurus
        
class PengurusForm(forms.ModelForm):
    class Meta:
        model = Pengurus
        fields = ['nama', 'jabatan', 'agenda']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Lengkap'}),
            'jabatan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Jabatan'}),
            'agenda': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Agenda Anda', 'rows': 3}),
        }
        labels = {
            'nama': 'Nama Lengkap',
            'jabatan': 'Jabatan',
            'agenda': 'Agenda',
        }