from django.core.management.base import BaseCommand

from apps.smartphones.models import (
    Brand,
    Smartphone,
    Chipset,
    PriceHistory,
)

from datetime import date



class Command(BaseCommand):

    help = "Create smartphone sample data"


    def handle(self, *args, **kwargs):


        smartphones_data = [

            {
                "brand": "Apple",
                "name": "iPhone 17 Pro",
                "release_date": date(2025, 9, 19),

                "chipset": {
                    "name": "Apple A19 Pro",
                    "antutu": 1800000,
                    "geekbench": 9000,
                },

                "ram": 12,
                "storage": 256,
                "storage_type": "ufs4_0",

                "battery": 3988,
                "charging": 40,

                "refresh": 120,
                "ppi": 460,

                "camera": 48,
                "ois": True,

                "price": 120000000,
            },


            {
                "brand": "Samsung",
                "name": "Galaxy S25 Ultra",
                "release_date": date(2025,1,22),

                "chipset": {
                    "name": "Snapdragon 8 Elite",
                    "antutu": 2100000,
                    "geekbench": 9500,
                },

                "ram":12,
                "storage":256,
                "storage_type":"ufs4_0",

                "battery":5000,
                "charging":45,

                "refresh":120,
                "ppi":505,

                "camera":200,
                "ois":True,

                "price":110000000,
            },


            {
                "brand":"Xiaomi",
                "name":"Xiaomi 15 Pro",
                "release_date":date(2024,10,29),

                "chipset":{
                    "name":"Snapdragon 8 Elite",
                    "antutu":2100000,
                    "geekbench":9500,
                },

                "ram":16,
                "storage":512,
                "storage_type":"ufs4_0",

                "battery":6100,
                "charging":90,

                "refresh":120,
                "ppi":520,

                "camera":50,
                "ois":True,

                "price":70000000,
            },


            {
                "brand":"Google",
                "name":"Pixel 10 Pro",
                "release_date":date(2025,8,20),

                "chipset":{
                    "name":"Google Tensor G5",
                    "antutu":1400000,
                    "geekbench":7000,
                },

                "ram":16,
                "storage":256,
                "storage_type":"ufs3_1",

                "battery":4870,
                "charging":30,

                "refresh":120,
                "ppi":495,

                "camera":50,
                "ois":True,

                "price":90000000,
            },


            {
                "brand":"OnePlus",
                "name":"OnePlus 13",
                "release_date":date(2025,1,7),

                "chipset":{
                    "name":"Snapdragon 8 Elite",
                    "antutu":2100000,
                    "geekbench":9500,
                },

                "ram":16,
                "storage":512,
                "storage_type":"ufs4_0",

                "battery":6000,
                "charging":100,

                "refresh":120,
                "ppi":510,

                "camera":50,
                "ois":True,

                "price":65000000,
            },

        ]


        for item in smartphones_data:


            brand, _ = Brand.objects.get_or_create(
                name=item["brand"]
            )


            chipset_data = item["chipset"]


            chipset, _ = Chipset.objects.get_or_create(
                name=chipset_data["name"],
                defaults={
                    "antutu_score": chipset_data["antutu"],
                    "geekbench_multi": chipset_data["geekbench"],
                }
            )


            smartphone, _ = Smartphone.objects.get_or_create(
                name=item["name"],
                brand=brand,
                defaults={

                    "release_date": item["release_date"],

                    "chipset": chipset,

                    "ram_gb": item["ram"],
                    "storage_gb": item["storage"],
                    "storage_type": item["storage_type"],

                    "battery_mah": item["battery"],
                    "fast_charging_w": item["charging"],

                    "display_refresh_hz": item["refresh"],
                    "display_ppi": item["ppi"],

                    "main_camera_mp": item["camera"],
                    "has_ois": item["ois"],

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