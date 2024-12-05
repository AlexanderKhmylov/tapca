from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.send_otp, name='send_otp'),
    path('login_verify/', views.verify_otp, name='verify_otp'),
    path(
        'logout/',
        LogoutView.as_view(next_page=reverse_lazy('cards:cards_main')),
        name='logout'),

    path(
        'user_profile/<int:pk>',
        views.UserProfileUpdateView.as_view(),
        name='user_profile'),
    path('user_setting/<int:pk>',
         views.UserSettingUpdateView.as_view(),
         name='user_setting'),
    path('statistics/<int:pk>', views.UserStatisticView.as_view(), name='statistics'),
    path('new_words/', views.MyNewWordsView.as_view(), name='new_words'),
    path('repeated_words/', views.my_repeated_word, name='repeated_words'),
    path('reset_progress/<int:user_card_id>', views.reset_progress, name='reset_progress'),
    path('delete_user_card/<int:user_card_id>', views.delete_user_card, name='delete_user_card'),
]
