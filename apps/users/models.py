from django.db import models
from apps.smartphones.models import Brand
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class UserPreference(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="preference"
    )


    min_price = models.PositiveBigIntegerField(
        null=True,
        blank=True
    )

    max_price = models.PositiveBigIntegerField(
        null=True,
        blank=True
    )


    camera_weight = models.PositiveIntegerField(
        default=50,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    battery_weight = models.PositiveIntegerField(
        default=50,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    performance_weight = models.PositiveIntegerField(
        default=50,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    display_weight = models.PositiveIntegerField(
        default=50,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )


    preferred_brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="preferred_users"
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


    class Meta:
        verbose_name = "User Preference"
        verbose_name_plural = "User Preferences"


    def __str__(self):
        return f"{self.user.username}'s preference"