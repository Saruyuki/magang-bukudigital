from django.db import models

# Create your models here.
class Pengurus(models.Model):
    nama = models.CharField(max_length=255)
    jabatan = models.CharField(max_length=100)
    agenda = models.TextField()
    tanggal_masuk = models.DateTimeField(auto_now_add=True)
