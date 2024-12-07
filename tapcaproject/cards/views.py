from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView

from .models import Card
from .service import get_user_cards
from users.models import UserCard
from cards.service import get_user_cards

# CARDS VIEW MODE ============================================================
class CardsView(TemplateView):
    template_name = 'cards/cards_main.html'


class CardRandomView(TemplateView):
    template_name = 'cards/card_random.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        card = (
            Card.objects.all()
            .filter(is_published=True)
            .prefetch_related('forms').order_by('?')[0]
        )
        context.update({
            'card': card,
        })
        return context


# CARDS LEARN VIEW ===========================================================
class CardsLearnView(LoginRequiredMixin, TemplateView):
    template_name = 'cards/cards_learn.html'


@login_required
def show_card_to_learn(request):
    cards = get_user_cards(request.user)
    if cards:
        card = cards.order_by('?')[0]
        return render(
            request, 'cards/card_to_learn.html', context={'card': card})

    return render(request, 'cards/no_cards.html', {})


@login_required
def save_card_to_repeat(request, card_id):
    frequency = request.GET.get('frequency')
    card = get_object_or_404(Card, pk=card_id)
    if not UserCard.objects.filter(card=card, user=request.user).exists():
        UserCard.objects.create(
            card=card, user=request.user, frequency=frequency)
    return show_card_to_learn(request)


class CardDetailView(DetailView):
    model = Card
    context_object_name = 'card'
    template_name = 'cards/one_card.html'
