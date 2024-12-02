from django.contrib.auth.models import AbstractUser
from django.db import models

from .config import OTP_SECRETE_MAX_LENGTH
from cards.models import Tag, Card


class TapcaUser(AbstractUser):
    email = models.EmailField(
        unique=True,
        verbose_name="Электронная почта",
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        verbose_name='Категории для изучения')
    is_student = models.BooleanField(
        default=True,
        verbose_name='Студент'
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'


class OTP(models.Model):
    user = models.OneToOneField(
        TapcaUser, on_delete=models.CASCADE, verbose_name='Пользователь',)
    otp_secret = models.CharField(
        max_length=OTP_SECRETE_MAX_LENGTH, verbose_name='Секрет',)

    def __str__(self):
        return f'{self.user} - {self.otp_secret}'

    class Meta:
        verbose_name = 'OTP'
        verbose_name_plural = 'OTPs'


class Progress(models.Model):
    user = models.ForeignKey(
        TapcaUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='progress',
    )
    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        verbose_name='Карточка',
        related_name='progress',
    )
    progress = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.user} - {self.card} - {self.progress}'

    class Meta:
        unique_together = ('user', 'card')
        ordering = ('user', 'progress')
        verbose_name = 'прогресс'
        verbose_name_plural = 'Прогресс'
