from django.db import models

# Create your models here.

class Tamu(models.Model):
    instansi = models.CharField(max_length=255)
    nama = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    provinsi = models.CharField(max_length=100)
    kota = models.CharField(max_length=100)
    keperluan = models.TextField()
    tanggal_kunjungan = models.DateTimeField(auto_now_add=True)
    
class Pengurus(models.Model):
    nama = models.CharField(max_length=255)
    jabatan = models.CharField(max_length=100)
    agenda = models.TextField()
    tanggal_masuk = models.DateTimeField(auto_now_add=True)
