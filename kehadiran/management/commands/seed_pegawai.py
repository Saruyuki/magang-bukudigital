from django.core.management.base import BaseCommand
from accounts.models import CustomUser
from kehadiran.models import Kehadiran
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Create 10 Pengurus entries using random users with role=pengurus (reuses users if fewer than 10)'

    def handle(self, *args, **options):
        fake = Faker('id_ID')

        # Get all users with role='pengurus'
        all_users = list(CustomUser.objects.all())

        if not all_users:
            self.stdout.write(self.style.ERROR('No users found in database.'))
            return

        total_to_create = 10
        created_count = 0

        for _ in range(total_to_create):
            # Pick a random user (even if reused)
            user = random.choice(all_users)

            # Create Pengurus entry
            Kehadiran.objects.create(
                nama=user.nama,
                jabatan=user.jabatan,
                agenda=fake.sentence(nb_words=6)
            )

            created_count += 1
            self.stdout.write(self.style.SUCCESS(f"Created Pengurus entry for {user.nama}"))

        self.stdout.write(self.style.SUCCESS(f"\nSuccessfully created {created_count} Pengurus entries."))
