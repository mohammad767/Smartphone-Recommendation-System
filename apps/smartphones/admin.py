from django.contrib import admin

# Register your models here.

from .models import (
    Brand,
    Smartphone,
    PriceHistory,
    SmartphoneSpecification,
    UserPreference
)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "created_at",
    )



@admin.register(Smartphone)
class SmartphoneAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "brand",
        "release_date",
    )

    search_fields = (
        "name",
        "brand__name",
    )



@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "smartphone",
        "price",
        "created_at",
    )



@admin.register(SmartphoneSpecification)
class SmartphoneSpecificationAdmin(admin.ModelAdmin):
    list_display = (
        "smartphone",
        "ram",
        "storage",
        "battery",
    )



@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "preferred_brand",
        "max_price",
    )