from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, OTPSession


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = [
        "phone",
        "full_name",
        "email",
        "is_staff",
        "is_active",
    ]

    search_fields = [
        "phone",
        "full_name",
        "email",
    ]

    list_filter = [
        "is_staff",
        "is_superuser",
        "is_active",
    ]

    ordering = ["phone"]

    # Explicitly list non-editable auto_now/auto_now_add fields here
    readonly_fields = (
        "created_at",
        "updated_at",
        "last_login",
    )

    fieldsets = (
        (None, {
            "fields": (
                "phone",
                "password",
            )
        }),
        ("Personal info", {
            "fields": (
                "full_name",
                "email",
                "birth_date",
                "profile_img",
            )
        }),
        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Important dates", {
            "fields": (
                "last_login",
                "created_at",
                "updated_at",
            )
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "phone",
                "password1",
                "password2",
                "is_active",
                "is_staff",
            ),
        }),
    )


