from django.core.management.base import BaseCommand
from buku.models import Tamu
from dashboard.utils import PROVINCE_NAMES
from faker import Faker 
import random

class Command(BaseCommand):
    help = 'Seed the database with random Tamu entries'
    
    def handle(self, *args, **options):
        fake = Faker('id_ID')
        
        for _ in range(50):
            instansi = fake.company()
            nama = fake.name()
            phone = fake.phone_number()
            email = fake.email()
            provinsi = random.choice(PROVINCE_NAMES)
            kota = fake.city()
            keperluan = random.choice(['Umum', 'Bisnis', 'Pribadi', 'Lainnya'])
            
            Tamu.objects.create(
                instansi=instansi,
                nama=nama,
                phone=phone,
                email=email,
                provinsi=provinsi,
                kota=kota,
                keperluan=keperluan,
            )
            
        self.stdout.write(self.style.SUCCESS('Successfully seeded the database with 50 Tamu entries'))