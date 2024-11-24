from django.views.generic import TemplateView, DetailView

from .models import Card


class CardsView(TemplateView):
    template_name = 'cards/cards_main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        card = Card.objects.all().prefetch_related('forms').order_by('?')[0]
        context.update({
            'card': card,
        })
        return context
