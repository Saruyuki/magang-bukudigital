from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'nama', 'jabatan', 'role']
    list_filter = ['role']
    search_fields = ['username', 'nama', 'jabatan']

admin.register(CustomUser, CustomUserAdmin)