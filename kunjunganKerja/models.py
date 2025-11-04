from django.db import models
from django.conf import settings

# Create your models here.

class Surat(models.Model):
    no_surat = models.CharField(max_length=255)
    file = models.FileField(upload_to='surat/')
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='uploaded_surats'
    )
    
    def __str__(self):
        return self.no_surat
    
class Kunjungan(models.Model):
    surat = models.ForeignKey(Surat, on_delete=models.CASCADE, related_name='kunjungan')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='kunjungan')
    
    no_surat = models.CharField(max_length=255)
    nama = models.CharField(max_length=255)
    jabatan = models.CharField(max_length=255)
    tujuan = models.CharField(max_length=255)
    agenda = models.TextField()
    
    tanggal_kunjungan = models.DateField()
    
    catatan_kunjungan = models.TextField(blank=True, null=True)
    foto_kunjungan = models.ImageField(upload_to='foto_kunjungan', null=True, blank=True)
    
    foto_lat = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    foto_lon = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    foto_datetime = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.nama} - {self.tanggal_kunjungan ({self.no_surat})}"
