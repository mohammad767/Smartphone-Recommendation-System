from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    model = User

    list_display = [
        "phone",
        "full_name",
        "is_staff",
        "is_active",
    ]

    ordering = [
        "phone"
    ]


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
            "classes": (
                "wide",
            ),

            "fields": (
                "phone",
                "password1",
                "password2",
                "is_active",
                "is_staff",
            ),
        }),
    )