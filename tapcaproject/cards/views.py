import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView

from .models import Card
from .service import get_user_cards
from users.models import UserCard
from cards.service import get_user_cards, get_user_repeated_cards
from .forms import CheckCardForm

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


# CARDS REPEAT VIEW ===========================================================
class CardsRepeatView(LoginRequiredMixin, TemplateView):
    template_name = 'cards/cards_repeat.html'

@login_required
def show_card_to_repeat(request):
    user_cards = get_user_repeated_cards(request.user)
    check_form = CheckCardForm()
    if user_cards:
        frequency = user_cards.values_list('frequency', flat=True)
        user_card = random.choices(user_cards, weights=frequency, k=1)[0]
        # user_cards = user_cards.order_by('?')[0]
        return render(
            request, 'cards/card_to_repeat.html', context={
                'user_card': user_card,
                'check_form': check_form,
            })

    return render(request, 'cards/no_cards_repeat.html', {})



@login_required
def know_card(request, user_card_id):
    user_card = get_object_or_404(UserCard, pk=user_card_id)
    if user_card.frequency > 10:
        user_card.frequency -= 1
        user_card.save()
    return show_card_to_repeat(request)


@login_required
def dont_know_card(request, user_card_id):
    user_card = get_object_or_404(UserCard, pk=user_card_id)
    if user_card.frequency < 100:
        user_card.frequency += 1
        user_card.save()
    return show_card_to_repeat(request)

@login_required
def check_card(request, card_id):
    word = ''
    if request.method == 'GET':
        form = CheckCardForm(request.GET)
        if form.is_valid():
            word = form.cleaned_data['word']
        card = get_object_or_404(Card, pk=card_id)
        if card.word == word:
            return render(request, 'cards/results_ok.html')
    return render(request, 'cards/results_ng.html')