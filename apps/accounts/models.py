import uuid

from datetime import timedelta

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin
)
from django.contrib.auth.hashers import (
    make_password,
    check_password
)
from django.core.validators import RegexValidator
from django.utils import timezone

from .managers import UserManager



PHONE_VALIDATOR = RegexValidator(
    regex=r"^(?:\+98[0-9]{10}|09[0-9]{9})$",
    message="Phone number must be in the format 09xxxxxxxxx"
)



class User(AbstractBaseUser, PermissionsMixin):

    phone = models.CharField(
        max_length=13,
        unique=True,
        validators=[PHONE_VALIDATOR]
    )


    full_name = models.CharField(
        max_length=100,
        blank=True
    )


    email = models.EmailField(
        unique=True,
        null=True,
        blank=True
    )


    birth_date = models.DateField(
        null=True,
        blank=True
    )


    profile_img = models.ImageField(
        upload_to="profiles/",
        null=True,
        blank=True
    )


    is_active = models.BooleanField(
        default=True
    )


    is_staff = models.BooleanField(
        default=False
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    updated_at = models.DateTimeField(
        auto_now=True
    )


    objects = UserManager()


    USERNAME_FIELD = "phone"

    REQUIRED_FIELDS = []


    def __str__(self):
        return self.phone
    
    
class OTPSession(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="otp_sessions"
    )


    otp_code_hash = models.CharField(
        max_length=128
    )


    temp_token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        db_index=True
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    expires_at = models.DateTimeField()


    is_used = models.BooleanField(
        default=False
    )


    cooldown_until = models.DateTimeField(
        null=True,
        blank=True
    )


    otp_request_attempts = models.PositiveIntegerField(
        default=0
    )


    otp_verify_attempts = models.PositiveIntegerField(
        default=0
    )


    MAX_ATTEMPTS = 4

    OTP_EXPIRY_MINUTES = 2

    COOLDOWN_MINUTES = 5



    class Meta:

        ordering = [
            "-created_at"
        ]

        indexes = [
            models.Index(
                fields=[
                    "user",
                    "is_used"
                ]
            )
        ]



    def save(self, *args, **kwargs):

        if not self.pk:

            self.expires_at = (
                timezone.now()
                +
                timedelta(
                    minutes=self.OTP_EXPIRY_MINUTES
                )
            )

        super().save(*args, **kwargs)



    def set_otp(self, plain_otp):

        self.otp_code_hash = make_password(
            plain_otp
        )



    def verify_otp(self, plain_otp):

        return check_password(
            plain_otp,
            self.otp_code_hash
        )



    def is_expired(self):

        return timezone.now() > self.expires_at



    def is_in_cooldown(self):

        if not self.cooldown_until:
            return False

        return timezone.now() < self.cooldown_until



    def apply_cooldown(self):

        self.cooldown_until = (
            timezone.now()
            +
            timedelta(
                minutes=self.COOLDOWN_MINUTES
            )
        )

        self.otp_verify_attempts = 0
        self.otp_request_attempts = 0

        self.save(
            update_fields=[
                "cooldown_until",
                "otp_verify_attempts",
                "otp_request_attempts"
            ]
        )



    def cooldown_remaining_seconds(self):

        if not self.is_in_cooldown():
            return 0

        return int(
            (
                self.cooldown_until
                -
                timezone.now()
            ).total_seconds()
        )



    def is_valid(self):

        return (
            not self.is_used
            and not self.is_expired()
            and not self.is_in_cooldown()
            and self.otp_verify_attempts < self.MAX_ATTEMPTS
        )



    def __str__(self):

        return f"OTP Session - {self.user.phone}"