import os

from dotenv import load_dotenv
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.shortcuts import get_object_or_404, reverse
from django.views.generic import UpdateView, TemplateView, ListView, FormView
from django_filters.views import FilterView
from django.core.exceptions import PermissionDenied

from .forms import OtpSendForm, OtpVerifyForm, UserProfileForm, UserSettingForm, UserSetForm
from .mixins import OnlyMyDataMixin
from .models import UserCard
from .service import create_otp, send_otp_email
from cards.models import Card, Tag
from cards.service import get_new_cards_of_user, get_user_cards
from cards.filters import CardFilter, UserCardFilter
from .config import WORD_PAGINATOR
from .service import get_client_ip

load_dotenv()
SMARTCAPTCHA_CLIENT_KEY = os.getenv('SMARTCAPTCHA_CLIENT_KEY')
User = get_user_model()

def login_captcha(request):
    error_message = ''
    if request.method == 'POST':
        token = request.POST.get('smart-token', None)
        if token:
            url = f"{reverse('users:send_otp')}?token={token}"
            return redirect(url)
        error_message = 'Ошибка верификации пользователя, попробуйте повторить попытку'

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
            url = f"{reverse('users:verify_otp')}?email={email}"
            return redirect(url)
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


# class UserProfileUpdateView(LoginRequiredMixin, OnlyMyDataMixin, UpdateView):
#     model = User
#     form_class = UserProfileForm
#     context_object_name = 'user'
#     template_name = 'users/user_profile_setting.html'
#
#     def get_success_url(self):
#         return reverse('cards:cards_main')


# class UserSettingUpdateView(LoginRequiredMixin, OnlyMyDataMixin, UpdateView):
#     model = User
#     form_class = UserSettingForm
#     context_object_name = 'user'
#     template_name = 'users/user_profile_setting.html'
#
#     def get_success_url(self):
#         return reverse('cards:cards_main')


class UserStatisticView(LoginRequiredMixin, OnlyMyDataMixin, UpdateView):
    model = User
    template_name = 'users/statistic_main.html'
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
        return reverse('users:statistics', kwargs={'pk': self.request.user.pk})


class MyNewWordsView(LoginRequiredMixin, FilterView):
    model = Card
    template_name = 'users/new_words.html'
    context_object_name = 'cards'
    filterset_class = CardFilter
    paginate_by = WORD_PAGINATOR

    def get_queryset(self):
        cards = get_new_cards_of_user(self.request.user)
        return cards


class MyRepeatedWordsView(LoginRequiredMixin, FilterView):
    model = Card
    template_name = 'users/repeated_words.html'
    context_object_name = 'cards'
    filterset_class = UserCardFilter
    paginate_by = WORD_PAGINATOR

    def get_queryset(self):
        cards = get_user_cards(self.request.user).order_by('-frequency')
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
    return render(request, 'users/statistics_words.html', context={'new_words': new_words, 'repeated_words': repeated_words, 'learned_words': learned_words})