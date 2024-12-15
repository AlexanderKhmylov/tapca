import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView
from django_filters.views import FilterView

from users.models import UserCard
from .models import Card
from .service import get_new_cards_of_user, get_user_cards, get_random_card
from .forms import CheckCardForm
from .cofig import SEARCH_LIMIT, MAX_FREQ, MID_FREQ, MIN_FREQ
from .filters import CardFilter


# CARDS RANDOM VIEW ===========================================================
class CardsRandomMainView(TemplateView):
    template_name = 'cards/cards_random.html'


class CardRandomView(TemplateView):
    template_name = 'cards/card_to_random.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'card': get_random_card()})
        return context


# CARDS LEARN VIEW ===========================================================
class CardsLearnView(LoginRequiredMixin, TemplateView):
    template_name = 'cards/cards_learn.html'


@login_required
def show_card_to_learn(request):
    cards = get_new_cards_of_user(request.user)
    if cards:
        card = cards.order_by('?')[0]
        return render(
            request, 'cards/card_to_learn.html', context={
                'card': card,
                'MAX_FREQ': MAX_FREQ,
                'MID_FREQ': MID_FREQ,
                'MIN_FREQ': MIN_FREQ,
            })

    return render(request, 'cards/no_cards.html', {})


@login_required
def save_card_to_repeat(request, card_id):
    frequency = request.GET.get('frequency', MAX_FREQ)
    card = get_object_or_404(Card, pk=card_id)
    if not UserCard.objects.filter(card=card, user=request.user).exists():
        UserCard.objects.create(
            card=card, user=request.user, frequency=frequency)
    return show_card_to_learn(request)


# CARDS REPEAT VIEW ===========================================================
class CardsRepeatView(LoginRequiredMixin, TemplateView):
    template_name = 'cards/cards_repeat.html'

@login_required
def show_card_to_repeat(request):
    user_cards = get_user_cards(request.user)
    check_form = CheckCardForm()
    if user_cards:
        frequencies = user_cards.values_list('frequency', flat=True)
        user_card = random.choices(user_cards, weights=frequencies, k=1)[0]
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


# CARDS DETAIL & SEARCH =======================================================
class CardDetailView(DetailView):
    model = Card
    context_object_name = 'card'
    template_name = 'cards/one_card.html'


class SearchWordsView(FilterView):
    model = Card
    template_name = 'cards/search_card.html'
    context_object_name = 'cards'
    filterset_class = CardFilter
    paginate_by = SEARCH_LIMIT

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)