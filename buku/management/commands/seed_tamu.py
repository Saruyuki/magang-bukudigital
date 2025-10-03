from django.core.management.base import BaseCommand
from buku.models import Tamu
from buku.utils import PROVINCE_NAMES
from faker import Faker 
from datetime import datetime, timedelta
import random
import string

class Command(BaseCommand):
    help = 'Seed the database with random Tamu entries'
    
    def handle(self, *args, **options):
        fake = Faker('id_ID')
        '''
        def generate_random_date(length=8):
            days_delta = random.randint(0, 30)
            return datetime.now() - timedelta(days=days_delta)'''
        
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