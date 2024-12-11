import os

from dotenv import load_dotenv
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth import login
from django.views.generic import UpdateView
from django_filters.views import FilterView

from .forms import OtpSendForm, OtpVerifyForm, UserSetForm
from .mixins import OnlyMyDataMixin
from .models import UserCard
from .service import create_otp, send_otp_email, get_client_ip
from cards.models import Card
from cards.service import get_new_cards_of_user, get_user_cards
from cards.filters import CardFilter, UserCardFilter
from .config import WORD_PAGINATOR

load_dotenv()
SMARTCAPTCHA_CLIENT_KEY = os.getenv('SMARTCAPTCHA_CLIENT_KEY')
User = get_user_model()

def login_captcha(request):
    error_message = ''
    if request.method == 'POST':
        token = request.POST.get('smart-token', None)
        if token:
            return redirect(f"{reverse('users:send_otp')}?token={token}")
        error_message = (
            'Ошибка верификации пользователя,'
            ' выполните задание и повторите попытку')
    return render(request, 'users/login.html', {
        'error_message': error_message,
        'SMARTCAPTCHA_CLIENT_KEY': SMARTCAPTCHA_CLIENT_KEY,
    })


def send_otp(request):
    if request.method == 'POST':
        form = OtpSendForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = get_object_or_404(User, email=email)
            code = create_otp(user)
            send_otp_email(user, code)
            return redirect(f"{reverse('users:verify_otp')}?email={email}")
    else:
        token = request.GET.get('token')
        user_ip = get_client_ip(request)
        form = OtpSendForm(initial={
            'token': token,
            'ip': user_ip,
        })
    return render(
        request, 'users/send_otp.html', {'form': form})


def verify_otp(request):
    if request.method == 'POST':
        form = OtpVerifyForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = get_object_or_404(User, email=email)
            login(request, user)
            return redirect('cards:cards_main')
    else:
        email = request.GET.get('email')
        form = OtpVerifyForm(initial={'email': email})

    return render(
        request, 'users/verify_otp.html', {'form': form})


class UserSettingsView(LoginRequiredMixin, OnlyMyDataMixin, UpdateView):
    model = User
    template_name = 'users/settings_main.html'
    form_class = UserSetForm
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        new_words_filter = CardFilter(
            self.request.GET,
            queryset=get_new_cards_of_user(self.request.user)
        )
        context['new_words_filter'] = new_words_filter

        repeated_words_filter = UserCardFilter(
            self.request.GET,
            queryset=get_user_cards(self.request.user)
        )
        context['repeated_words_filter'] = repeated_words_filter
        return context

    def get_success_url(self):
        return reverse(
            'users:settings', kwargs={'pk': self.request.user.pk})


class MyNewWordsView(LoginRequiredMixin, FilterView):
    template_name = 'users/new_words.html'
    context_object_name = 'cards'
    filterset_class = CardFilter
    paginate_by = WORD_PAGINATOR

    def get_queryset(self):
        cards = get_new_cards_of_user(self.request.user)
        return cards


class MyRepeatedWordsView(LoginRequiredMixin, FilterView):
    template_name = 'users/repeated_words.html'
    context_object_name = 'cards'
    filterset_class = UserCardFilter
    paginate_by = WORD_PAGINATOR

    def get_queryset(self):
        cards = get_user_cards(self.request.user)
        return cards


def reset_progress(request, user_card_id):
    user_card = get_object_or_404(UserCard, pk=user_card_id)
    user_card.frequency = 100
    user_card.save()
    response = MyRepeatedWordsView.as_view()(request)
    response.headers['HX-Trigger'] = 'update_statistics'
    return response


def delete_user_card(request, user_card_id):
    user_card = get_object_or_404(UserCard, pk=user_card_id)
    user_card.delete()
    response = MyRepeatedWordsView.as_view()(request)
    response.headers['HX-Trigger'] = 'update_statistics'
    return response


def get_statistic(request):
    new_words = get_new_cards_of_user(request.user).count()
    repeated_words = get_user_cards(request.user).count()
    learned_words = get_user_cards(request.user).filter(frequency=10).count()
    return render(
        request,
        'users/statistics_words.html',
        context={
            'new_words': new_words,
            'repeated_words': repeated_words,
            'learned_words': learned_words}
    )
