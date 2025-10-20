from django import forms
from .models import Kehadiran
        
class KehadiranForm(forms.ModelForm):
    class Meta:
        model = Kehadiran
        fields = ['nama', 'jabatan', 'agenda']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'jabatan': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'agenda': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Agenda Anda', 'rows': 3}),
        }
        labels = {
            'nama': 'Nama Lengkap',
            'jabatan': 'Jabatan',
            'agenda': 'Agenda',
        }
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['nama'].initial = user.nama
            self.fields['jabatan'].initial = user.jabatan