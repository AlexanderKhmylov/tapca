from django.urls import path

from . import views

app_name = 'cards'

urlpatterns = [
    path('', views.CardsView.as_view(), name='cards_main'),
    path('card_random/', views.CardRandomView.as_view(), name='card_random'),
    path('learn/', views.CardsLearnView.as_view(), name='cards_learn'),
    path('card_to_learn/', views.show_card_to_learn, name='card_to_learn'),
    path('save_to_repeat/<int:card_id>', views.save_card_to_repeat, name='save_card_to_repeat'),
    path('card/<slug:slug>', views.CardDetailView.as_view(), name='card_detail'),
]
