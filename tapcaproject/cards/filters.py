import django_filters
from django.db.models import Q

from .models import Card
from users.models import UserCard




class CardFilter(django_filters.FilterSet):
    word = django_filters.CharFilter(method='filter_word', label='Поиск')

    class Meta:
        model = Card
        fields = ('word',)

    def filter_word(self, queryset, name, value):
        return queryset.filter(
            Q(word__icontains=value) |
            Q(translation__icontains=value) |
            Q(translation_secondary__icontains=value)
        )


class UserCardFilter(django_filters.FilterSet):
    card = django_filters.CharFilter(method='filter_card', label='Поиск')

    class Meta:
        model = UserCard
        fields = ('card',)

    def filter_card(self, queryset, name, value):
        return queryset.filter(
            Q(card__word__icontains=value) |
            Q(card__translation__icontains=value) |
            Q(card__translation_secondary__icontains=value)
        )
