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
                