from django import forms
from django.contrib.auth import get_user_model
        
User = get_user_model()

class SingleUserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan password'}),
        label="Password"
    )
    
    class Meta:
        model = User
        fields = ['username', 'password', 'nama', 'jabatan', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan username'}),
            'nama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan nama lengkap'}),
            'jabatan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan jabatan'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': 'Username',
            'nama': 'Nama Lengkap',
            'jabatan': 'Jabatan',
            'role': 'Peran',
        }
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
        
class BulkUserUploadForm(forms.Form):
    file = forms.FileField(help_text="Upload file .csv atau .xlsx berisi data user")