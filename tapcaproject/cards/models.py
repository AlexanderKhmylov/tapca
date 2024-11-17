from django.db import models

class Card(models.Model):
    word = models.CharField(
        max_length=128,
        unique=True,
        verbose_name='Слово'
    )
    transcription = models.CharField(
        max_length=128,
        verbose_name='Транскрипция',
        blank=True,
        null=True
    )
    translation = models.TextField(verbose_name='Перевод')

    def __str__(self):
        return self.word

    class Meta:
        ordering = ('word',)
        verbose_name = 'карточка'
        verbose_name_plural = 'Карточки'
