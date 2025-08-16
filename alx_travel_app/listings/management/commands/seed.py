from django.core.management.base import BaseCommand
from listings.models import Listing
import random

class Command(BaseCommand):
    help = 'Seed the database with sample listing data'

    def handle(self, *args, **kwargs):
        sample_locations = ['Nairobi', 'Mombasa', 'Zanzibar', 'Kigali', 'Cape Town']
        sample_titles = ['Ocean View Apartment', 'Mountain Retreat', 'City Center Flat']

        for i in range(10):
            Listing.objects.create(
                title=random.choice(sample_titles),
                description='Sample description for listing',
                price_per_night=round(random.uniform(50.0, 500.0), 2),
                location=random.choice(sample_locations)
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded 10 listings'))
