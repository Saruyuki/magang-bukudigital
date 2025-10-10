from django.core.management.base import BaseCommand
from kehadiran.models import Pengurus
from faker import Faker 
import random
import string

class Command(BaseCommand):
    help = 'Seed the database with random Pengurus entries'
    
    def handle(self, *args, **options):
        fake = Faker('id_ID')
        
        for _ in range(10):
            nama = fake.name()
            jabatan = fake.job()
            agenda = fake.sentence(nb_words=6)
                        
            Pengurus.objects.create(
                nama=nama,
                jabatan=jabatan,
                agenda=agenda    
            )
           
        self.stdout.write(self.style.SUCCESS('Successfully seeded the database with 10 Pegawai entries'))