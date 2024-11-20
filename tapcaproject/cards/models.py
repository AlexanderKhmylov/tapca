from django.db import models


class Tag(models.Model):
    COLOR_CHOICES = [
        ('GREEN', 'Зеленый'),
        ('RED', 'Красный'),
        ('ORANGE', 'Оранжевый'),
        ('BLUE', 'Синий'),
        ('GRAY', 'Серый'),
    ]
    name = models.CharField(max_length=128, unique=True, verbose_name='Тег')
    color = models.CharField(max_length=16, choices=COLOR_CHOICES, verbose_name='Цвет')

    def __str__(self):
        return f'{self.name} - {self.color}'

    class Meta:
        ordering = ('name',)
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'




class Card(models.Model):

    PART_OF_SPEECH_CHOICES = [
        ('verb', 'глагол'),
        ('interjection', 'междометие'),
        ('pronoun', 'местоимение'),
        ('adverb', 'наречие'),
        ('preposition', 'предлог'),
        ('adjective', 'прилагательное'),
        ('conjunction', 'союз'),
        ('noun', 'существительное'),
    ]

    word = models.CharField(
        max_length=128,
        unique=True,
        verbose_name='Слово'
    )
    part_of_speech = models.CharField(
        max_length=32, choices=PART_OF_SPEECH_CHOICES, verbose_name='Часть речи')
    tag = models.ManyToManyField(Tag, verbose_name='Тег')
    transcription = models.CharField(
        max_length=128,
        verbose_name='Транскрипция',
        blank=True,
        null=True
    )
    translation = models.TextField(verbose_name='Перевод')

    def __str__(self):
        return f'{self.word} - {self.part_of_speech}'

    class Meta:
        ordering = ('word',)
        verbose_name = 'карточка'
        verbose_name_plural = 'Карточки'


