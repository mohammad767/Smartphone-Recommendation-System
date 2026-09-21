from django.contrib import admin

from .models import (
    Brand,
    Chipset,
    Smartphone,
    PriceHistory,
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



@admin.register(Chipset)
class ChipsetAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "antutu_score",
        "geekbench_multi",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "-antutu_score",
    )

    list_per_page = 20



@admin.register(Smartphone)
class SmartphoneAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "brand",
        "chipset",
        "release_date",
        "created_at",
    )

    search_fields = (
        "name",
        "brand__name",
        "chipset__name",
    )

    list_filter = (
        "brand",
        "chipset",
        "release_date",
    )

    autocomplete_fields = (
        "brand",
        "chipset",
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