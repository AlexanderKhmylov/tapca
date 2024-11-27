TAG_MAX_LENGTH = 128
COLOR_MAX_LENGTH = 16
COLOR_LIST = [
        ('GREEN', 'Зеленый'),
        ('RED', 'Красный'),
        ('ORANGE', 'Оранжевый'),
        ('BLUE', 'Синий'),
        ('GRAY', 'Серый'),
    ]

PART_OF_SPEECH_LIST = [
        ('verb', 'глагол'),
        ('interjection', 'междометие'),
        ('pronoun', 'местоимение'),
        ('adverb', 'наречие'),
        ('preposition', 'предлог'),
        ('adjective', 'прилагательное'),
        ('conjunction', 'союз'),
        ('noun', 'существительное'),
    ]
WORD_MAX_LENGTH = 128
PART_OF_SPEECH_MAX_LENGTH = 32
TRANSCRIPTION_MAX_LENGTH = 128

FORM_LIST = [
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
TYPE_MAX_LENGTH = 32
FORM_MAX_LENGTH = 256

ENG_MAX_LENGTH = 256
RUS_MAX_LENGTH = 256
