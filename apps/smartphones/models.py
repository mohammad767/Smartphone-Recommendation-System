from django.db import models



class Brand(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


    class Meta:
        ordering = ["name"]
        verbose_name = "Brand"
        verbose_name_plural = "Brands"


    def __str__(self):
        return self.name



class Smartphone(models.Model):

    name = models.CharField(
        max_length=200
    )

    release_date = models.DateField(
        null=True,
        blank=True
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        related_name="smartphones"
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


    class Meta:
        ordering = ["-release_date"]
        verbose_name = "Smartphone"
        verbose_name_plural = "Smartphones"

        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["brand"]),
        ]


    def __str__(self):
        return f"{self.brand.name} {self.name}"



class PriceHistory(models.Model):

    smartphone = models.ForeignKey(
        Smartphone,
        on_delete=models.CASCADE,
        related_name="price_history"
    )

    price = models.PositiveBigIntegerField()


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Price History"
        verbose_name_plural = "Price Histories"

        indexes = [
            models.Index(fields=["smartphone", "-created_at"]),
        ]


    def __str__(self):
        return f"{self.smartphone.name} - {self.price}"



class SmartphoneSpecification(models.Model):

    DISPLAY_TYPE = (
        ("LCD", "LCD"),
        ("IPS", "IPS"),
        ("OLED", "OLED"),
        ("AMOLED", "AMOLED"),
    )


    smartphone = models.OneToOneField(
        Smartphone,
        on_delete=models.CASCADE,
        related_name="specification"
    )


    ram = models.PositiveIntegerField(
        help_text="GB"
    )

    storage = models.PositiveIntegerField(
        help_text="GB"
    )

    battery = models.PositiveIntegerField(
        help_text="mAh"
    )

    camera = models.PositiveIntegerField(
        help_text="Megapixel"
    )

    display_type = models.CharField(
        max_length=10,
        choices=DISPLAY_TYPE
    )

    processor = models.CharField(
        max_length=100
    )

    weight = models.PositiveIntegerField(
        help_text="Gram"
    )


    class Meta:
        verbose_name = "Smartphone Specification"
        verbose_name_plural = "Smartphone Specifications"


    def __str__(self):
        return f"{self.smartphone.name} Specification"



