from django.contrib import admin
from .models import UserPreference
# Register your models here.


@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "preferred_brand",
        "max_price",
        "camera_weight",
        "battery_weight",
        "performance_weight",
    )

    search_fields = (
        "user__username",
    )

    list_filter = (
        "preferred_brand",
    )

    autocomplete_fields = (
        "user",
        "preferred_brand",
    )