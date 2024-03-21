from django.core.management.base import BaseCommand
from exercises.models import Pet  # Adjust this import to your model's location
import random

class Command(BaseCommand):
    help = 'Clears existing pets and populates the database with 300 random pets'

    def handle(self, *args, **options):
        # Warning: This will delete all existing pets!
        self.stdout.write(self.style.WARNING('Clearing existing pets from the database...'))
        Pet.objects.all().delete()

        types_of_pet = ['Dog', 'Cat', 'Bird', 'Fish']
        cities = ['Springfield', 'Shelbyville', 'Ogdenville']
        states = ['NY', 'CA', 'TX', 'FL']
        names = ['Buddy', 'Bella', 'Charlie', 'Lucy']

        for _ in range(300):
            Pet.objects.create(
                name=random.choice(names),
                age=random.randint(1, 15),
                streetnumber=str(random.randint(1, 9999)),
                city=random.choice(cities),
                zipcode=str(random.randint(10000, 99999)),
                state=random.choice(states),
                typeofpet=random.choice(types_of_pet),
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully repopulated the database with 300 pets'))

