from .models import Card
from users.models import UserCard


def get_user_repeated_cards(user):
    return UserCard.objects.filter(user=user)


def get_user_cards(user):
    tags = user.tags.all().values_list('pk', flat=True)
    cards_to_repeat = get_user_repeated_cards(user).values_list('card_id', flat=True)
    cards = (
        Card.objects
        .filter(is_published=True)
        .filter(tag__in=tags)
        .prefetch_related('forms')
        .exclude(pk__in=cards_to_repeat)
    ).distinct()
    return cards
