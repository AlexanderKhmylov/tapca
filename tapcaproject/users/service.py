import pyotp
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import OTP
from .config import OTP_DIGITS, OTP_VALID_INTERVAL_SEC


def create_otp(user):
    # Generate Secret and Code
    otp_secret = pyotp.random_base32()
    otp = pyotp.TOTP(
        otp_secret,
        digits=OTP_DIGITS,
        interval=OTP_VALID_INTERVAL_SEC
    )
    otp_code = otp.now()

    # Save OTP to the database
    otp_obj, created = OTP.objects.get_or_create(user=user)
    otp_obj.otp_secret = otp_secret
    otp_obj.save()
    print(f'{otp_code=}')
    return otp_code


def send_otp_email(user, code):
    text_content = render_to_string(
        'emails/2fa.txt',
        context={'OTP': code},
    )

    # Secondly, render the HTML content.
    html_content = render_to_string(
        'emails/2fa.html',
        context={'OTP': code},
    )

    # Then, create a multipart email instance.
    msg = EmailMultiAlternatives(
        'Код подтверждения',
        text_content,
        'noreply@tapca.ru',
        [user.email],
        headers={},
    )

    # Lastly, attach the HTML content to the email instance and send.
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def verify_otp_code(user, code):
    otp_obj = get_object_or_404(OTP, user=user)
    otp = pyotp.TOTP(
        otp_obj.otp_secret,
        digits=OTP_DIGITS,
        interval=OTP_VALID_INTERVAL_SEC
    )
    return otp.verify(code, valid_window=1)
