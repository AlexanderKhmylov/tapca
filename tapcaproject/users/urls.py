from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView

from . import views

app_name = 'users'

urlpatterns = [
    path('login_captcha/', views.login_captcha, name='login_captcha'),
    path('login_email/', views.send_otp, name='send_otp'),
    path('login_verify/', views.verify_otp, name='verify_otp'),
    path(
        'logout/',
        LogoutView.as_view(next_page=reverse_lazy('cards:cards_main')),
        name='logout'),
    # SETTINGS MENU ==========================================================
    path(
        'settings/<int:pk>',
        views.UserSettingsView.as_view(),
        name='settings'),
    path(
        'new_words/',
        views.MyNewWordsView.as_view(),
        name='new_words'),
    path(
        'repeated_words/',
        views.MyRepeatedWordsView.as_view(),
        name='repeated_words'),
    path(
        'reset_progress/<int:user_card_id>',
        views.reset_progress,
        name='reset_progress'),
    path(
        'delete_user_card/<int:user_card_id>',
        views.delete_user_card,
        name='delete_user_card'),
    path(
        'words_statistics/',
        views.get_statistic,
        name='words_statistics'),
]
