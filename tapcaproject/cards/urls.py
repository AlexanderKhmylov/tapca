from django.urls import path

from . import views

app_name = 'cards'

urlpatterns = [
    path('card/<slug:slug>', views.CardDetailView.as_view(), name='card_detail'),
    path('card_search', views.SearchWordsView.as_view(), name='card_search'),

    path('', views.CardsView.as_view(), name='cards_main'),
    path('card_random/', views.CardRandomView.as_view(), name='card_random'),

    path('learn/', views.CardsLearnView.as_view(), name='cards_learn'),
    path('card_to_learn/', views.show_card_to_learn, name='card_to_learn'),
    path('save_to_repeat/<int:card_id>', views.save_card_to_repeat, name='save_card_to_repeat'),

    path('repeat/', views.CardsRepeatView.as_view(), name='cards_repeat'),
    path('card_to_repeat/', views.show_card_to_repeat, name='card_to_repeat'),
    path('know_card/<int:user_card_id>', views.know_card, name='know_card'),
    path('dont_know_card/<int:user_card_id>', views.dont_know_card, name='dont_know_card'),
    path('check_card/<int:card_id>', views.check_card, name='check_card'),
]
