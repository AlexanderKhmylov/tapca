from django.urls import path

from . import views

app_name = 'cards'

urlpatterns = [
    path('', views.CardsView.as_view(), name='cards_main'),
    path('card_random/', views.CardRandomView.as_view(), name='card_random'),

]
