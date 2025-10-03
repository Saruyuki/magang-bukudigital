from django.core.management.base import BaseCommand
from buku.models import Pegawai
from faker import Faker 
import random
import string

class Command(BaseCommand):
    help = 'Seed the database with random Pegawai entries'
    
    def handle(self, *args, **options):
        fake = Faker('id_ID')
        
        def generate_kode(length=8):
            return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        
        for _ in range(10):
            nama = fake.name()
            jabatan = fake.job()
            agenda = fake.sentence(nb_words=6)
                        
            Pegawai.objects.create(
                nama=nama,
                jabatan=jabatan,
                agenda=agenda    
            )
           
        self.stdout.write(self.style.SUCCESS('Successfully seeded the database with 10 Pegawai entries'))