import os
import json

from dotenv import load_dotenv
import pyotp
import requests
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from .models import OTP
from .config import OTP_DIGITS, OTP_VALID_INTERVAL_SEC


load_dotenv()
SMARTCAPTCHA_SERVER_KEY = os.getenv('SMARTCAPTCHA_SERVER_KEY')
IS_PRODUCTION = settings.IS_PRODUCTION

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
    if not IS_PRODUCTION:
        print(f'{otp_code=}')
    return otp_code


def send_otp_email(user, code):
    text_content = render_to_string(
        'emails/2fa.txt',
        context={'OTP': code},
    )
    html_content = render_to_string(
        'emails/2fa.html',
        context={'OTP': code},
    )
    msg = EmailMultiAlternatives(
        'Код подтверждения',
        text_content,
        'noreply@tapca.ru',
        [user.email],
        headers={},
    )
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


def check_captcha(token, user_ip):
    resp = requests.post(
       "https://smartcaptcha.yandexcloud.net/validate",
       data={
          "secret": SMARTCAPTCHA_SERVER_KEY,
          "token": token,
          "ip": user_ip
       },
       timeout=1
    )
    server_output = resp.content.decode()
    if resp.status_code != 200:
       # print(f"Allow access due to an error: code={resp.status_code}; message={server_output}", file=sys.stderr)
       return True
    return json.loads(server_output)["status"] == "ok"


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
