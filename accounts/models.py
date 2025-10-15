from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    nama = models.CharField(max_length=255)
    jabatan = models.CharField(max_length=255)
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('pengurus', 'Pengurus'),
    )
    role = models.CharField(max_length=10,choices=ROLE_CHOICES, default='pengurus')
    
    def __str__(self):
        return self.nama or self.username