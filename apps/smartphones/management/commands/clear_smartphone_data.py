from django.core.management.base import BaseCommand

from apps.smartphones.models import (
    Smartphone,
    PriceHistory,
    Brand,
    Chipset,
)


class Command(BaseCommand):

    help = "Delete smartphone test data"


    def handle(self, *args, **kwargs):

        PriceHistory.objects.all().delete()
        Smartphone.objects.all().delete()
        Chipset.objects.all().delete()
        Brand.objects.all().delete()


        self.stdout.write(
            self.style.SUCCESS(
                "Smartphone data deleted successfully"
            )
        )