from django import forms
from .models import Kunjungan

class KunjunganForm(forms.ModelForm):
    class Meta:
        model = Kunjungan
        fields = [ 
            'no_surat', 'nama', 'jabatan', 'tujuan', 'agenda',
            'tanggal_kunjungan', 'catatan_kunjungan', 
        ]
        widgets = {
            'no_surat': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
            'nama': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
            'jabatan': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
            'tujuan': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
            'agenda': forms.Textarea(attrs={'readonly': 'readonly', 'rows': 2, 'class': 'form-control'}),
            'tanggal_kunjungan': forms.DateInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
            'catatan_kunjungan': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        localized_fields = ()
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user :
            self.fields['nama'].initial = user.nama
            self.fields['jabatan'].initial = user.jabatan
    