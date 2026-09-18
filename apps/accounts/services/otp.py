import random

from django.utils import timezone

from apps.accounts.models import User, OTPSession



def generate_otp():
   
    return str(
        random.randint(
            100000,
            999999
        )
    )



def create_otp_session(user):

    otp_code = generate_otp()

    otp_session = OTPSession(
        user=user
    )

    otp_session.set_otp(
        otp_code
    )

    otp_session.save()


    return {
        "temp_token": otp_session.temp_token,
        "otp": otp_code
    }


def verify_otp(temp_token, otp):
    
    session = OTPSession.objects.get(
        temp_token=temp_token
    )

    if not session.is_valid():
        return None


    if not session.verify_otp(otp):
        session.otp_verify_attempts += 1
        session.save()

        return None


    session.is_used = True
    session.save()


    return session.user