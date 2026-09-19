from django.contrib import admin

from .models import (
    Brand,
    Smartphone,
    PriceHistory,
    SmartphoneSpecification,
)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "created_at",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "name",
    )

    list_per_page = 20



@admin.register(Smartphone)
class SmartphoneAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "brand",
        "release_date",
        "created_at",
    )

    search_fields = (
        "name",
        "brand__name",
    )

    list_filter = (
        "brand",
        "release_date",
    )

    autocomplete_fields = (
        "brand",
    )

    ordering = (
        "-release_date",
    )

    list_per_page = 20



@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):

    list_display = (
        "smartphone",
        "price",
        "created_at",
    )

    search_fields = (
        "smartphone__name",
    )

    list_filter = (
        "created_at",
    )

    autocomplete_fields = (
        "smartphone",
    )

    ordering = (
        "-created_at",
    )



@admin.register(SmartphoneSpecification)
class SmartphoneSpecificationAdmin(admin.ModelAdmin):

    list_display = (
        "smartphone",
        "ram",
        "storage",
        "battery",
        "display_type",
    )

    search_fields = (
        "smartphone__name",
        "processor",
    )

    list_filter = (
        "display_type",
        "ram",
        "storage",
    )

    autocomplete_fields = (
        "smartphone",
    )



