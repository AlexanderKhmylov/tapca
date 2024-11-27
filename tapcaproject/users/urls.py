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
]
