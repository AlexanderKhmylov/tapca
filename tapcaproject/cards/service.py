from .models import Card
from users.models import UserCard


def get_active_cards():
    return (
        Card.objects.all().filter(is_published=True).prefetch_related('forms'))


def get_random_card():
    return get_active_cards().order_by('?')[0]


def get_user_cards(user):
    return UserCard.objects.filter(user=user)


def get_new_cards_of_user(user):
    tags = user.tags.all().values_list('pk', flat=True)
    user_cards_id_to_repeat = get_user_cards(user).values_list(
        'card_id', flat=True)
    return (
        get_active_cards()
        .filter(tag__in=tags)
        .exclude(pk__in=user_cards_id_to_repeat)
    ).distinct()
