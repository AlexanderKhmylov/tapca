from django.db import models
from django.urls import reverse


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
        verbose_name='Слово'
    )
    part_of_speech = models.CharField(
        max_length=32,
        choices=PART_OF_SPEECH_CHOICES,
        verbose_name='Часть речи')
    tag = models.ManyToManyField(Tag, verbose_name='Тег')
    transcription = models.CharField(
        max_length=128,
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

    # def get_absolute_url(self):
    #     return reverse('cards:card_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.word} - {self.part_of_speech}'

    class Meta:
        ordering = ('word',)
        verbose_name = 'карточка'
        verbose_name_plural = 'Карточки'


class Form(models.Model):

    FORM_CHOICES = [
        ('1_n_singular', 'Единственное число'),
        ('2_n_plural', 'Множественное число'),

        ('1_v_base_form', 'Инфинитив (базовая форма)'),
        ('2_v_past_simple', 'Прошедшее время'),
        ('3_v_past_participle', 'Причастие прошедшего времени'),
        ('4_v_present_participle', 'Причастие настоящего времени'),
        ('5_v_third_person_singular', '3 лицо, ед. число, наст. время'),

        ('1_a_regular', 'Основная форма'),
        ('2_a_comparative', 'Сравнительная степень'),
        ('3_a_superlative', 'Превосходная степень'),
    ]

    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        related_name='forms',
        verbose_name='Слово'
    )
    type = models.CharField(
        max_length=32,
        choices=FORM_CHOICES,
        verbose_name='Тип'
    )
    form = models.CharField(max_length=256, verbose_name='Форма')


class Example(models.Model):
    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        related_name='examples',
        verbose_name='Слово'
    )
    eng = models.CharField(
        max_length=256,
        verbose_name='English'
    )
    rus = models.CharField(
        max_length=256,
        verbose_name='Russian'
    )
