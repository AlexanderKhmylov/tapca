from random import randint

from django.views.generic import TemplateView, DetailView

from .models import Card


class CardsView(TemplateView):
    template_name = 'cards/cards_main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_cards = Card.objects.count()
        random_card = randint(0, total_cards-1)
        card = Card.objects.all()[random_card:].first()
        context.update({
            'card': card,
        })
        return context
