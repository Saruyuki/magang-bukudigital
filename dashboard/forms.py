from django import forms
from django.contrib.auth import get_user_model
        
User = get_user_model()

class SingleUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'nama', 'jabatan', 'role']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'jabatan': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
        
class BulkUserUploadForm(forms.Form):
    file = forms.FileField(help_text="Upload file .csv atau .xlsx berisi data user")