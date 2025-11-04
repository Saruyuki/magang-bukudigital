from django.core.management.base import BaseCommand
from accounts.models import CustomUser

class Command(BaseCommand):
    help = 'Create test users: admin and pengurus'
    
    def handle(self, *args, **kwargs):
        if not CustomUser.objects.filter(username='pengurus').exists():
            CustomUser.objects.create_user(
                username='pengurus',
                password='pengurus123',
                nama='Alfin',
                jabatan='Pengurus',
                role='pengurus',
            )
            self.stdout.write(self.style.SUCCESS('Created pengurus'))
            
        if not CustomUser.objects.filter(username='admin').exists():
            CustomUser.objects.create_superuser(
                username='admin',
                password='admin123',
                nama='Daus',
                jabatan='Admin',
                role='admin',
            )
            self.stdout.write(self.style.SUCCESS('Created admin'))
            
    
        if not CustomUser.objects.filter(username='pengurus1').exists():
            CustomUser.objects.create_user(
                username='pengurus1',
                password='pengurus123',
                nama='Dr. Jajang Sugiat',
                jabatan='Ketua Bidang Humas',
                role='pengurus',
            )
            self.stdout.write(self.style.SUCCESS('Created pengurus'))
        
        if not CustomUser.objects.filter(username='pengurus2').exists():
            CustomUser.objects.create_user(
                username='pengurus2',
                password='pengurus123',
                nama='Agus Indra Arisandi, S.H.I',
                jabatan='Ketua Bidang Pendidikan & Penataran',
                role='pengurus',
            )
            self.stdout.write(self.style.SUCCESS('Created pengurus'))
        
        if not CustomUser.objects.filter(username='pengurus3').exists():
            CustomUser.objects.create_user(
                username='pengurus3',
                password='pengurus123',
                nama='Dr. Asep Angga Permadi, M.Pd.',
                jabatan='Wk. Bidang Prestasi',
                role='pengurus',
            )
            self.stdout.write(self.style.SUCCESS('Created pengurus'))
        
        if not CustomUser.objects.filter(username='pengurus4').exists():
            CustomUser.objects.create_user(
                username='pengurus4',
                password='pengurus123',
                nama='Mirwan Aji Soleh, S.Pd., M.Pd.',
                jabatan='Wk. Bidang Rencana Strategis',
                role='pengurus',
            )
            self.stdout.write(self.style.SUCCESS('Created pengurus'))
            
        if not CustomUser.objects.filter(username='pengurus5').exists():
            CustomUser.objects.create_user(
                username='pengurus5',
                password='pengurus123',
                nama='M. Romdhon, S.E., M.Si., AK., CA.',
                jabatan='Wk. Bendahara',
                role='pengurus',
            )
            self.stdout.write(self.style.SUCCESS('Created pengurus'))
                