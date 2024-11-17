from django.contrib.auth.models import AbstractUser


class TapcaUser(AbstractUser):
    class Meta:
        ordering = ('username',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
