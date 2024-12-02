from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView

from .models import Card


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


def show_card(request):
    if request.user.is_authenticated:
        card = ...

    return render(request, 'cards/no_cards.html', {})
