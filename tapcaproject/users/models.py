from django.contrib.auth.models import AbstractUser
from django.db import models

from tapcaproject.users.config import OTP_SECRETE_MAX_LENGTH


class TapcaUser(AbstractUser):
    class Meta:
        ordering = ('username',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'


class OTP(models.Model):
    user = models.OneToOneField(
        TapcaUser, on_delete=models.CASCADE, verbose_name='Пользователь',)
    otp_secret = models.CharField(max_length=OTP_SECRETE_MAX_LENGTH, verbose_name='Секрет',)

    def __str__(self):
        return f'{self.user} - {self.otp_secret}'

    class Meta:
        verbose_name = 'OTP'
        verbose_name_plural = 'OTP'
