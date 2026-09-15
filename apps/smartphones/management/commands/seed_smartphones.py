from django.core.management.base import BaseCommand
from apps.smartphones.models import (
    Brand,
    Smartphone,
    SmartphoneSpecification,
    PriceHistory
)
from datetime import date


class Command(BaseCommand):

    help = "Create sample smartphone data"


    def handle(self, *args, **kwargs):

        smartphones_data = [
            {
                "brand": "Apple",
                "name": "iPhone 17 Pro",
                "release_date": date(2025, 9, 19),
                "ram": 12,
                "storage": 256,
                "battery": 3988,
                "camera": 48,
                "display_type": "OLED",
                "processor": "Apple A19 Pro",
                "weight": 206,
                "price": 120000000,
            },

            {
                "brand": "Samsung",
                "name": "Galaxy S25 Ultra",
                "release_date": date(2025, 1, 22),
                "ram": 12,
                "storage": 256,
                "battery": 5000,
                "camera": 200,
                "display_type": "AMOLED",
                "processor": "Snapdragon 8 Elite",
                "weight": 218,
                "price": 110000000,
            },

            {
                "brand": "Xiaomi",
                "name": "Xiaomi 15 Pro",
                "release_date": date(2024, 10, 29),
                "ram": 16,
                "storage": 512,
                "battery": 6100,
                "camera": 50,
                "display_type": "AMOLED",
                "processor": "Snapdragon 8 Elite",
                "weight": 219,
                "price": 70000000,
            },

            {
                "brand": "Google",
                "name": "Pixel 10 Pro",
                "release_date": date(2025, 8, 20),
                "ram": 16,
                "storage": 256,
                "battery": 4870,
                "camera": 50,
                "display_type": "OLED",
                "processor": "Google Tensor G5",
                "weight": 207,
                "price": 90000000,
            },

            {
                "brand": "OnePlus",
                "name": "OnePlus 13",
                "release_date": date(2025, 1, 7),
                "ram": 16,
                "storage": 512,
                "battery": 6000,
                "camera": 50,
                "display_type": "AMOLED",
                "processor": "Snapdragon 8 Elite",
                "weight": 210,
                "price": 65000000,
            },
        ]


        for item in smartphones_data:

            brand, created = Brand.objects.get_or_create(
                name=item["brand"]
            )


            smartphone, created = Smartphone.objects.get_or_create(
                name=item["name"],
                brand=brand,
                defaults={
                    "release_date": item["release_date"]
                }
            )


            SmartphoneSpecification.objects.get_or_create(
                smartphone=smartphone,
                defaults={
                    "ram": item["ram"],
                    "storage": item["storage"],
                    "battery": item["battery"],
                    "camera": item["camera"],
                    "display_type": item["display_type"],
                    "processor": item["processor"],
                    "weight": item["weight"],
                }
            )


            PriceHistory.objects.create(
                smartphone=smartphone,
                price=item["price"]
            )


        self.stdout.write(
            self.style.SUCCESS(
                "Smartphone test data created successfully"
            )
        )