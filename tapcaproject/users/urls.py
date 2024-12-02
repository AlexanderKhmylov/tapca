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
]
