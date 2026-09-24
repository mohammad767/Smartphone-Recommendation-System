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



class Chipset(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    antutu_score = models.PositiveIntegerField(
        help_text="AnTuTu v10 benchmark score"
    )

    geekbench_multi = models.PositiveIntegerField(
        null=True,
        blank=True
    )


    class Meta:
        ordering = ["name"]
        verbose_name = "Chipset"
        verbose_name_plural = "Chipsets"


    def __str__(self):
        return self.name



class Smartphone(models.Model):
    

    DISPLAY_TYPE = (
        ("OLED","OLED"),
        ("IPS","IPS",),
        ("LCD","LCD"),
        ("AMOLED","AMOLED"),
        ("S-AMOLED","S-AMOLED")
        
    )

    name = models.CharField(
        max_length=200
    )


    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        related_name="smartphones"
    )


    release_date = models.DateField(
        null=True,
        blank=True
    )


    chipset = models.ForeignKey(
        Chipset,
        on_delete=models.PROTECT,
        related_name="smartphones"
    )


    # Performance

    ram_gb = models.PositiveSmallIntegerField()

    storage_gb = models.PositiveIntegerField()


    storage_type = models.CharField(
        max_length=20,
        choices=[
            ("emmc", "eMMC"),
            ("ufs2_2", "UFS 2.2"),
            ("ufs3_1", "UFS 3.1"),
            ("ufs4_0", "UFS 4.0"),
        ]
    )


    # Battery

    battery_mah = models.PositiveIntegerField()

    fast_charging_w = models.PositiveIntegerField(
        default=0
    )


    

    display_refresh_hz = models.PositiveSmallIntegerField()

    display_ppi = models.PositiveIntegerField()
    
    display_type = models.CharField(max_length=10,choices=DISPLAY_TYPE)




    main_camera_mp = models.PositiveIntegerField()



    performance_score = models.FloatField(
        default=0
    )

    battery_score = models.FloatField(
        default=0
    )

    display_score = models.FloatField(
        default=0
    )

    camera_score = models.FloatField(
        default=0
    )
    
    
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
    


    class Meta:

        ordering = [
            "-release_date"
        ]

        verbose_name = "Smartphone"
        verbose_name_plural = "Smartphones"

        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["brand"]),
            models.Index(fields=["performance_score"]),
            models.Index(fields=["camera_score"]),
            models.Index(fields=["display_score"]),
            models.Index(fields=["battery_score"])
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

        ordering = [
            "-created_at"
        ]

        verbose_name = "Price History"
        verbose_name_plural = "Price Histories"


        indexes = [
            models.Index(
                fields=[
                    "smartphone",
                    "-created_at"
                ]
            ),
        ]


    def __str__(self):
        return f"{self.smartphone.name} - {self.price}"