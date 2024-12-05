from django.db import models

from .cofig import (
    TAG_MAX_LENGTH, COLOR_MAX_LENGTH, COLOR_CHOICES, PART_OF_SPEECH_CHOICES,
    WORD_MAX_LENGTH, PART_OF_SPEECH_MAX_LENGTH, TRANSCRIPTION_MAX_LENGTH,
    FORM_CHOICES, TYPE_MAX_LENGTH, FORM_MAX_LENGTH, ENG_MAX_LENGTH,
    RUS_MAX_LENGTH
)


class Tag(models.Model):
    name = models.CharField(
        max_length=TAG_MAX_LENGTH, unique=True, verbose_name='Тег')
    color = models.CharField(
        max_length=COLOR_MAX_LENGTH, choices=COLOR_CHOICES, verbose_name='Цвет')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ('name',)
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'


class Card(models.Model):
    word = models.CharField(
        max_length=WORD_MAX_LENGTH,
        verbose_name='Слово'
    )
    part_of_speech = models.CharField(
        max_length=PART_OF_SPEECH_MAX_LENGTH,
        choices=PART_OF_SPEECH_CHOICES,
        verbose_name='Часть речи')
    tag = models.ManyToManyField(Tag, verbose_name='Тег')
    transcription = models.CharField(
        max_length=TRANSCRIPTION_MAX_LENGTH,
        verbose_name='Транскрипция',
        blank=True,
        null=True
    )
    translation = models.TextField(verbose_name='Перевод')
    translation_secondary = models.TextField(
        blank=True,
        null=True,
        verbose_name='Перевод дополнительный')
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг'
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name='Опубликована'
    )

    # TODO:
    # def get_absolute_url(self):
    #     return reverse('cards:card_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.word} ({self.part_of_speech})'

    class Meta:
        ordering = ('word',)
        verbose_name = 'карточка'
        verbose_name_plural = 'Карточки'


class Form(models.Model):
    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        related_name='forms',
        verbose_name='Слово'
    )
    type = models.CharField(
        max_length=TYPE_MAX_LENGTH,
        choices=FORM_CHOICES,
        verbose_name='Тип'
    )
    form = models.CharField(
        max_length=FORM_MAX_LENGTH, verbose_name='Форма')

    def __str__(self):
        return f'{self.card} - {self.type} - {self.form}'

    class Meta:
        ordering = ('type',)
        verbose_name = 'форма'
        verbose_name_plural = 'Формы'


class Example(models.Model):
    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        related_name='examples',
        verbose_name='Слово'
    )
    eng = models.TextField(
        max_length=ENG_MAX_LENGTH,
        verbose_name='English'
    )
    rus = models.TextField(
        max_length=RUS_MAX_LENGTH,
        verbose_name='Russian'
    )

    def __str__(self):
        return f'{self.card} - {self.eng} - {self.rus}'
